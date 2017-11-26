from django.db import models

# Create your models here.
from yukuz.models import Person


class DeviceType(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return self.title


class MobDevice(models.Model):
    user_id = models.ForeignKey(Person, null=False)
    device = models.CharField(max_length=512, primary_key=True)
    type = models.ForeignKey(DeviceType)
    dev_version = models.CharField(max_length=50)
    is_driver = models.BooleanField(default=False)
    added = models.DateTimeField(auto_created=True, auto_now_add=True)

    def __str__(self):
        return str(self.user_id.user)
