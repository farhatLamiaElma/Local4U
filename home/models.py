from django.db import models
from accounts.models import Farmer
# Create your models here.
# FAQ model
class FAQs(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.question
