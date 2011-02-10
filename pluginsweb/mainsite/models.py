from django.db import models
from django.contrib.auth.models import User


class Plugin(models.Model):
    '''Aranduka plugin uploaded to the web.'''
    name = models.CharField(max_length=50)
    version = models.CharField(max_length=20)
    description = models.TextField()
    uploaded = models.DateTimeField()
    user = models.ForeignKey(User)
    file = models.FileField(upload_to='plugins')
