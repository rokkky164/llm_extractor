FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt \
    && python -m nltk.downloader punkt averaged_perceptron_tagger

COPY . .

EXPOSE 8000

CMD ["gunicorn", "llm_extractor.wsgi:application", "--bind", "0.0.0.0:8000"]

