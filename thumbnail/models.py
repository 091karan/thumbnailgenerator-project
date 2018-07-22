import os
from django.db import models

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(BASE_DIR,'thumbnail')

class Thumb(models.Model):
    type = models.TextField()
    media = models.FileField()
    thumbnailcreated = models.ImageField()

    def __str__(self):
        return '{}'.format(self.type)
