from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Analysis
from .serializers import AnalysisSerializer
from .utils import extract_keywords, analyze_with_llm

@api_view(["POST"])
def analyze(request):
    text = request.data.get("text", "").strip()
    if not text:
        return Response({"error": "Input text is empty"}, status=400)

    keywords = extract_keywords(text)
    llm_result = analyze_with_llm(text)

    if "error" in llm_result:
        return Response({"error": llm_result["error"]}, status=500)

    analysis = Analysis.objects.create(
        text=text,
        summary=llm_result["summary"],
        title=llm_result.get("title"),
        topics=llm_result["topics"],
        sentiment=llm_result["sentiment"],
        keywords=keywords,
    )
    serializer = AnalysisSerializer(analysis)
    return Response(serializer.data, status=201)


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
