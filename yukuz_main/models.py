from django.db import models

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from yukuz_oauth.models import UUser
# Create your models here.
# will create once user register or sign up.
from yukuz_oauth.models import Person, Driver


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        print("token: " + UUser(sender).username)
        from rest_framework.authtoken.models import Token
        token = Token.objects.create(user=instance)
        print("not created")
        return token
    return None


class VehicleType(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=300)

    def __str__(self):
        return self.title


class Car(models.Model):
    car_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    number = models.CharField(max_length=15, primary_key=True)
    min_kg = models.PositiveIntegerField(default=1)
    max_kg = models.PositiveIntegerField(default=5)
    # image = models.ImageField(upload_to='vehicles/', default='def_user.png')
    by_person = models.ForeignKey('yukuz_oauth.Person', on_delete=models.CASCADE)

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

    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'


class PostOrder(models.Model):
    post_title = models.CharField(max_length=200)

    description = models.CharField(max_length=3000)

    weigth = models.FloatField(null=False)

    source_address = models.CharField(max_length=300)

    destination_address = models.CharField(max_length=300)

    is_picked = models.BooleanField(default=False)

    deadline = models.DateField(null=False, )

    currency_type = models.ForeignKey(PriceClass, null=False, on_delete=models.CASCADE)

    estimated_price = models.FloatField(default=0, null=False)

    type_of_vehicle = models.ForeignKey('VehicleType', null=False, on_delete=models.CASCADE)

    is_cancelled = models.BooleanField(default=False)

    order_by = models.ForeignKey(Person, verbose_name="order by a person", on_delete=models.CASCADE)

    order_time = models.DateTimeField(auto_now_add=True)

    def delete(self, using=None, keep_parents=False):
        # self.order_image.delete()
        super(PostOrder, self).delete(using=None, keep_parents=False)

    def __str__(self):
        return str(self.order_by.ssn) + self.post_title


class OrderImages(models.Model):
    order = models.ForeignKey(PostOrder, related_name='order_image', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/", default="def_user.png")

    def __str__(self):
        return "image" + self.order.__str__()


class PickedOrder(models.Model):
    order = models.ForeignKey(PostOrder, on_delete=models.CASCADE)
    picked_by = models.ManyToManyField('yukuz_oauth.Driver', blank=True, )
    picked_time = models.DateTimeField(auto_now_add=True)

    def delete(self, using=None, keep_parents=False):
        # post = PostOrder.objects.get(pk=self.order)
        # post.is_picked = False
        # post.save()
        self.order.is_picked = False
        self.order.save()
        super(PickedOrder, self).delete(using=None, keep_parents=False)

    def __str__(self):
        return self.order.post_title


class DeliveringProcess(models.Model):
    picked_order = models.ForeignKey('PickedOrder', related_name='delivering_process', on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(Driver, on_delete=models.CASCADE)
    is_finished = models.BooleanField(default=False)
    start_time = models.DateTimeField(auto_now=True)
    end_time = models.DateTimeField(blank=True, null=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        order = PostOrder.objects.get(pk=self.picked_order.order_id)
        order.is_picked = True
        order.save()
        super(DeliveringProcess, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return str(self.picked_order) + " " + self.assigned_to.driver.user.username

    class Meta:
        verbose_name_plural = 'Delivering Processes'


class DriverRate(models.Model):
    star = models.PositiveIntegerField(default=0)
    star_for = models.ForeignKey('DeliveringProcess', on_delete=models.CASCADE)
    star_by = models.ForeignKey(Person, on_delete=models.CASCADE)
    description = models.TextField(default="")

    def __str__(self):
        return str(self.star) + " " + self.description
