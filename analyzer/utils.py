import nltk
import openai
import json
from collections import Counter

# Make sure you download once
# nltk.download("punkt")
# nltk.download("averaged_perceptron_tagger")

def extract_keywords(text):
    words = nltk.word_tokenize(text.lower())
    tagged = nltk.pos_tag(words)
    nouns = [word for word, pos in tagged if pos.startswith("NN")]
    common = Counter(nouns).most_common(3)
    return [w for w, _ in common]


def analyze_with_llm(text: str):
    prompt = f"""
    Summarize the following text in 1–2 sentences and extract as JSON:
    {{
        "summary": "...",
        "title": "...",
        "topics": ["...", "...", "..."],
        "sentiment": "positive/neutral/negative"
    }}
    Text: {text}
    """
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        content = resp["choices"][0]["message"]["content"]
        return json.loads(content)
    except Exception as e:
        return {"error": str(e)}
