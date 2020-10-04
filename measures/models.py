from django.db import models
from users.models import User

class Measure(models.Model):
    class Meta:
        db_table = 'measures'

    value = models.FloatField(editable=False, null=True, blank=True)
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.value)
