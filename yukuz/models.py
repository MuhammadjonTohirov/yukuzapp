from django.db import models


# Create your models here.
class Person(models.Model):
    ssn = models.IntegerField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    joined_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.ssn) + " " + self.first_name + " " + self.last_name


class VehicleType(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=300)

    def __str__(self):
        return self.title


class Car(models.Model):
    car_type = models.OneToOneField(VehicleType)
    number = models.CharField(max_length=15)
    min_kg = models.PositiveIntegerField(default=1)
    max_kg = models.PositiveIntegerField(default=5)

    def __str__(self):
        return self.car_type.title + " " + str(self.number)


class Driver(models.Model):
    driver = models.OneToOneField(Person)
    car = models.ManyToManyField(Car)
    reg_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.driver.first_name


class Baggage(models.Model):
    height = models.FloatField(default=10)
    width = models.FloatField(default=10)
    length = models.FloatField(default=10)
    weigth = models.FloatField(default=0)
    

class PostOrder(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=3000)
    source_address = models.CharField(max_length=300)
    destination_address = models.CharField(max_length=300)
    # image = models.FileField()
    order_by = models.OneToOneField(Person, on_delete=models.CASCADE, verbose_name="order by a person")
    order_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order_by.ssn) + self.title


class PickedOrder(models.Model):
    order = models.OneToOneField(Driver)
    picked_by = models.OneToOneField(Person)
    picked_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.picked_by.ssn)
