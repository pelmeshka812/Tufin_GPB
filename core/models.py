from django.db import models


class Rule(models.Model):
    id = models.AutoField(primary_key=True)
    source = models.CharField(max_length=500)
    destination = models.CharField(max_length=500)
    port = models.IntegerField()
    comment = models.CharField(max_length=500, blank=True)
    protocol = models.CharField(max_length=500, blank=True)
    status = models.CharField(max_length=50, blank=True)  # choices
    message = models.CharField(max_length=500, blank=True)
    last_update = models.DateTimeField()

    def get_absolute_url(self):
        return "/rules/%i/" % self.id


class File(models.Model):
    excel = models.FileField(upload_to='excel/')
