from django.db import models
from django.utils import timezone

class BaseModel(models.Model):

    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

