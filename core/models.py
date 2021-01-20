from django.db import models


class Rule(models.Model):
    jid = models.AutoField(primary_key=True)
    source = models.CharField(max_length=500)
    destination = models.CharField(max_length=500)
    # path = models.CharField(max_length=500)
    port = models.IntegerField()
    comment = models.CharField(max_length=500)
    protocol = models.CharField(max_length=500)
    status = models.CharField(max_length=50, blank=True)  # choices


class File(models.Model):
    excel = models.FileField()
