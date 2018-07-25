import os
from django.db import models

class Thumb(models.Model):
    type = models.TextField()
    media = models.FileField()
    thumbnailcreated = models.ImageField()

    def __str__(self):
        return '{}'.format(self.type)
