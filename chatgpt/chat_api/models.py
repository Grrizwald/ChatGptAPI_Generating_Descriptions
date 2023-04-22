from django.db import models

class Past(models.Model):
    question = models.CharField(max_length=250)
    answer = models.TextField(max_length=7000)
    
    def __str__(self):
        return self.question
