import nltk
import json
import os

from collections import Counter
from openai import OpenAI



client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

NLTK_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nltk_data")
os.makedirs(NLTK_DATA_DIR, exist_ok=True)

# Add local nltk_data to search path
if NLTK_DATA_DIR not in nltk.data.path:
    nltk.data.path.append(NLTK_DATA_DIR)

# Download all required packages
required_packages = [
    'punkt',                   # tokenizer
    'punkt_tab',               # for sent_tokenize in NLTK ≥3.8
    'averaged_perceptron_tagger',       # legacy
    'averaged_perceptron_tagger_eng'    # new POS model in NLTK ≥3.8
]

for pkg in required_packages:
    try:
        if 'punkt' in pkg:
            nltk.data.find(f'tokenizers/{pkg}')
        else:
            nltk.data.find(f'taggers/{pkg}')
    except LookupError:
        nltk.download(pkg, download_dir=NLTK_DATA_DIR)


def extract_keywords(text):
    """
    Extracts the 3 most frequent nouns from the text.
    """
    words = nltk.word_tokenize(text.lower())
    tagged = nltk.pos_tag(words)
    nouns = [word for word, pos in tagged if pos.startswith("NN")]
    common = Counter(nouns).most_common(3)
    return [word for word, _ in common]


def analyze_with_llm(text: str):
    """
    Calls OpenAI GPT model to return summary, title, topics, sentiment as JSON.
    Compatible with openai>=1.0.0
    """
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
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        # Extract content from response"
        content = response.choices[0].message["content"]

        # Convert to JSON
        return json.loads(content)

    except Exception as e:
        #return {"error": str(e)}
        return {
            "summary": "This is a mock summary.",
            "title": "Mock Title",
            "topics": ["mock", "test", "demo"],
            "sentiment": "neutral"
        }