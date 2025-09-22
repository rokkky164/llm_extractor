from django.db.models import (
    Model,
    TextField,
    CharField,
    JSONField,
    DateTimeField
)
from django.utils import timezone


class Analysis(Model):
    text = TextField()
    summary = TextField()
    title = CharField(max_length=255, null=True, blank=True)
    topics = JSONField(default=list)
    sentiment = CharField(max_length=20)
    keywords = JSONField(default=list)
    confidence = FloatField(default=0.0)
    created_at = DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Analysis {self.id} - {self.title or 'Untitled'}"
