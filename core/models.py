from django.db import models


class Rule(models.Model):
    uid = models.AutoField(primary_key=True)
    source = models.CharField(max_length=500)
    destination = models.CharField(max_length=500)
    path = models.CharField(max_length=500)
    status = models.CharField(max_length=50, blank=True)
