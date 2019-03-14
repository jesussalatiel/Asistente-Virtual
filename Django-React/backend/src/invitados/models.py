from django.db import models
from mongoengine import Document, EmbeddedDocument, fields

# Create your models here.
class Invitado(models.Model):
    
    title = models.CharField(max_length = 120)
    content = models.TextField()

    def __str__(self):
        return self.title


class ToolInput(EmbeddedDocument):
    name = fields.StringField(required=True)
    value = fields.DynamicField(required=True)


class Tool(Document):
    label = fields.StringField(required=True)
    description = fields.StringField(required=True, null=True)
    inputs = fields.ListField(fields.EmbeddedDocumentField(ToolInput))
