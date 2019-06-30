from django.db import models

# Create your models here.
from yukuz_oauth.models import Person


class DeviceType(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return self.title


class MobDevice(models.Model):
    user_id = models.ForeignKey(Person, null=False, on_delete=models.CASCADE)
    device = models.CharField(max_length=512, primary_key=True)
    type = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    token = models.CharField(max_length=50)
    is_driver = models.BooleanField(default=False)
    added = models.DateTimeField(auto_created=True, auto_now_add=True)

    def dict(self):
        return {
            'user': self.user_id.user.username,
            'token': self.token,
            'is_driver': self.is_driver,
            'creation_date': self.added
        }

    def __str__(self):
        return str(self.user_id.user)
