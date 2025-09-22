from django.test import TestCase
from rest_framework.test import APIClient


class AnalyzerTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_analyze_single_text(self):
        response = self.client.post("/api/analyze", {"text": "OpenAI released GPT-5."}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn("summary", response.data[0])
        self.assertIn("confidence", response.data[0])

    def test_analyze_batch_texts(self):
        texts = ["First text about AI.", "Second text about Python."]
        response = self.client.post("/api/analyze", {"texts": texts}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.data), 2)
        for r in response.data:
            self.assertIn("confidence", r)

    def test_empty_input(self):
        response = self.client.post("/api/analyze", {"text": ""}, format='json')
        self.assertEqual(response.status_code, 400)
