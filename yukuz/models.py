from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

# Create your models here.
# will create once user register or sign up.
from yukuz_auth.models import Person, Driver


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# class UserAvatar(models.Model):
#     owner = models.OneToOneField('Person', primary_key=True, related_name='ava')
#     image = models.ImageField(verbose_name='image/def_user', default='def_user')
#
#     def __str__(self):
#         return str(self.owner_id) + " " + str(self.image)


# Person class


class VehicleType(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=300)

    def __str__(self):
        return self.title


class Car(models.Model):
    car_type = models.ForeignKey(VehicleType)
    title = models.CharField(max_length=50)
    number = models.CharField(max_length=15, primary_key=True)
    min_kg = models.PositiveIntegerField(default=1)
    max_kg = models.PositiveIntegerField(default=5)
    # image = models.ImageField(upload_to='vehicles/', default='def_user.png')
    by_person = models.ForeignKey('yukuz_auth.Person')

    def description(self):
        return "The car (" + str(self.number) + ") can deliver baggage from " + str(self.min_kg) + " to " + str(
            self.max_kg)

    def __str__(self):
        return self.car_type.title + " " + str(self.number)


class PriceClass(models.Model):
    title = models.CharField(max_length=50)
    sign = models.CharField(max_length=15)

    def __str__(self):
        return self.title


class PostOrder(models.Model):
    post_title = models.CharField(max_length=200)
    description = models.CharField(max_length=3000)
    weigth = models.FloatField(null=False)
    source_address = models.CharField(max_length=300)
    destination_address = models.CharField(max_length=300)
    is_picked = models.BooleanField(default=False)
    deadline = models.DateField(null=False, )
    currency_type = models.ForeignKey(PriceClass, null=False)
    estimated_price = models.FloatField(default=0, null=False)
    type_of_vehicle = models.ForeignKey('VehicleType', null=False)
    is_cancelled = models.BooleanField(default=False)
    order_by = models.ForeignKey(Person, verbose_name="order by a person")
    order_time = models.DateTimeField(auto_now_add=True)

    def delete(self, using=None, keep_parents=False):
        # self.order_image.delete()
        super(PostOrder, self).delete(using=None, keep_parents=False)

    def __str__(self):
        return str(self.order_by.ssn) + self.post_title


class OrderImages(models.Model):
    order = models.ForeignKey(PostOrder, related_name='order_image')
    image = models.ImageField(upload_to="images/", default="def_user.png")

    def __str__(self):
        return "image" + self.order.__str__()


class PickedOrder(models.Model):
    order = models.OneToOneField(PostOrder, related_name='picked_order')
    picked_by = models.ForeignKey('yukuz_auth.Driver', )
    picked_time = models.DateTimeField(auto_now_add=True)

    def delete(self, using=None, keep_parents=False):
        # post = PostOrder.objects.get(pk=self.order)
        # post.is_picked = False
        # post.save()
        self.order.is_picked = False
        self.order.save()
        super(PickedOrder, self).delete(using=None, keep_parents=False)

    def __str__(self):
        return str(self.picked_by.driver.ssn)


class DriverRate(models.Model):
    star = models.PositiveIntegerField(default=0)
    star_for = models.ForeignKey(PickedOrder)
    star_by = models.ForeignKey(Person)
    description = models.TextField(default="")

    def __str__(self):
        return str(self.star) + " " + self.description

#
# class OrderImages(models.Model):
#     order = models.ForeignKey(PostOrder)
#     image = models.ImageField(default='images/def_user.png', upload_to='images')
#
#     def __str__(self):
#         return str(self.pk) + " - " + str(self.order)
