from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Person(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='person', on_delete=models.CASCADE,
                                primary_key=True)
    ssn = models.IntegerField()
    image = models.ImageField(verbose_name='image/def_user', default='def_user')
    phone_number = models.CharField(max_length=15)
    joined_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.ssn) + " " + self.user.first_name + " " + self.user.last_name

    def delete(self, using=None, keep_parents=False):
        # self.ava.delete()
        # if self.driver is not None:
        #     self.driver.delete()
        super(Person, self).delete(using=None, keep_parents=False)


class Driver(models.Model):
    driver = models.OneToOneField(Person, on_delete=models.CASCADE, primary_key=True, related_name='driver')
    description = models.TextField(max_length=500, verbose_name="About driver")
    driver_license = models.ImageField(upload_to='licenses/', null=False)
    is_active = models.BooleanField(default=True)
    reg_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.driver.user.first_name
