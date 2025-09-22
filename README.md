### Setup & Run Instructions

Clone and install dependencies

git clone <repo-url>
cd llm_extractor
pip install -r requirements.txt


Install NLTK corpora (first run only)

python -m nltk.downloader punkt averaged_perceptron_tagger


Configure environment

Create a .env file or set an environment variable:

export OPENAI_API_KEY="your_api_key_here"


Run database migrations

python manage.py makemigrations
python manage.py migrate


Start the server

python manage.py runserver


### Test the API

POST /api/analyze → Analyze new text
Example:

{ "text": "OpenAI released a new model today that improves reasoning." }


GET /api/search?topic=openai → Search analyses by topic/keyword


### Batch Processing

- POST multiple texts at once:
```json
{
  "texts": [
    "First text about AI.",
    "Second text about Python."
  ]
}