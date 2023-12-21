from django.db import models

# Create your models here.


class Model(models.Model):
    name = models.TextField()
    title = models.TextField(null=True)
    son = models.TextField(null=True)

