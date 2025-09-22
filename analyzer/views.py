from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Analysis
from .serializers import AnalysisSerializer
from .utils import extract_keywords, analyze_with_llm


@api_view(["POST"])
def analyze(request):
    texts = request.data.get("texts")  # batch support
    if not texts:
        single_text = request.data.get("text", "").strip()
        if not single_text:
            return Response({"error": "Input text is empty"}, status=400)
        texts = [single_text]

    results = []
    for text in texts:
        keywords = extract_keywords(text)
        llm_result = analyze_with_llm(text)
        if "error" in llm_result:
            results.append({"text": text, "error": llm_result["error"]})
            continue

        confidence = compute_confidence(llm_result)

        analysis = Analysis.objects.create(
            text=text,
            summary=llm_result["summary"],
            title=llm_result.get("title"),
            topics=llm_result["topics"],
            sentiment=llm_result["sentiment"],
            keywords=keywords,
            confidence=confidence
        )
        results.append(AnalysisSerializer(analysis).data)
    return Response(results, status=201)


@api_view(["GET"])
def search(request):
    topic = request.query_params.get("topic")
    if not topic:
        return Response({"error": "Missing topic query"}, status=400)

    analyses = Analysis.objects.filter(
        models.Q(topics__icontains=topic) | models.Q(keywords__icontains=topic)
    )
    serializer = AnalysisSerializer(analyses, many=True)
    return Response(serializer.data)


def compute_confidence(data):
    score = len(data.get("topics", [])) * 0.3 + min(len(data.get("summary", "")) / 100, 1) * 0.7
    return round(score, 2)
