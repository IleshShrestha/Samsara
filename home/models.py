from django.db import models
import os
from uuid import uuid4
from django.conf import settings


def path_making(path):
    def __init__(self, path):
        self.path = path

    def __call__(self, filename):
        renaming(filename)
        return os.path.join(self.path, filename)
    

def renaming():
    def __call__(self, instance, filename):
        # splits the extension and filename
        ext = filename.split('.')[-1]
        if instance.pk:
            filename = f'{instance.pk}.{ext}'
        else:
            # set filename as random string
            filename = f'{uuid4.hex}.{ext}'
        return filename


# contact
class contact(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    description = models.CharField(max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to=path_making(settings.MEDIA_ROOT + 'uploads/contact'))

    def __str__(self):
        return self.image
    

