from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings


# Create your models here.
# will create once user register or sign up.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Image(models.Model):
    image = models.ImageField(verbose_name='image')


# Person class
class Person(models.Model):
    # def get_short_name(self):
    #     return self.first_name
    #
    # def get_full_name(self):
    #     return self.first_name + " " + self.last_name
    user = models.OneToOneField('auth.User', related_name='person', on_delete=models.CASCADE)
    ssn = models.IntegerField()
    avatar = models.ImageField(verbose_name='human avatar', default='images/def_user.png', upload_to='images/')
    # first_name = models.CharField(max_length=50)
    # last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    # email = models.EmailField()
    joined_date = models.DateTimeField(auto_now_add=True)

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['email']

    def __str__(self):
        return str(self.ssn) + " " + self.user.first_name + " " + self.user.last_name


class VehicleType(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=300)

    def __str__(self):
        return self.title


class DeviceType(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return self.title


class Device(models.Model):
    user_id = models.OneToOneField(User)
    device = models.CharField(max_length=512)
    type = models.OneToOneField(DeviceType)
    dev_version = models.CharField(max_length=50)
    is_driver = models.BooleanField(default=False)
    added = models.DateTimeField(auto_created=True, auto_now_add=True)

    def __str__(self):
        return str(self.user_id.id)


class Car(models.Model):
    car_type = models.OneToOneField(VehicleType)
    number = models.CharField(max_length=15)
    min_kg = models.PositiveIntegerField(default=1)
    max_kg = models.PositiveIntegerField(default=5)

    def description(self):
        return "The car (" + str(self.number) + ") can deliver baggage from " + str(self.min_kg) + " to " + str(
            self.max_kg)

    def __str__(self):
        return self.car_type.title + " " + str(self.number)


class Driver(models.Model):
    driver = models.OneToOneField(Person)
    avatar = models.ImageField(verbose_name="driver avatar", default="def_user.png")
    car = models.ForeignKey(Car)
    reg_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.driver.user.first_name


class PostOrder(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=3000)
    weigth = models.FloatField(null=False)
    source_address = models.CharField(max_length=300)
    destination_address = models.CharField(max_length=300)
    is_picked = models.BooleanField(default=False)
    # image = models.FileField()
    order_by = models.ForeignKey(Person, verbose_name="order by a person")
    order_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order_by.ssn) + self.title


class PickedOrder(models.Model):
    order = models.OneToOneField(PostOrder)
    picked_by = models.ForeignKey(Driver, parent_link=True)
    picked_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.picked_by.driver.ssn)


class DriverRate(models.Model):
    star = models.PositiveIntegerField(default=0)
    star_for = models.ForeignKey(PickedOrder)
    star_by = models.ForeignKey(Person)
    description = models.TextField(default="")

    def __str__(self):
        return str(self.star) + " " + self.description
