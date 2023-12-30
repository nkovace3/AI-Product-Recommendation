from django.db import models

class Recommendation(models.Model):
    user = models.CharField(max_length=30)
    rec1 = models.CharField(max_length=30)
    rec2 = models.CharField(max_length=30)
    rec3 = models.CharField(max_length=30)
    rec4 = models.CharField(max_length=30)
    rec5 = models.CharField(max_length=30)
    rec6 = models.CharField(max_length=30)
    rec7 = models.CharField(max_length=30)
    rec8 = models.CharField(max_length=30)
    rec9 = models.CharField(max_length=30)
    rec10 = models.CharField(max_length=30)


# Create your models here.
