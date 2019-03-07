from django.conf import settings
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.core.validators import RegexValidator


# Create your models here.

class UBaseManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone_number, password):
        if not password or not phone_number:
            raise ValueError("you need to set phone number and password ")

        user = self.model(
            phone_number=phone_number
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password):
        user = self.create_user(
            phone_number=phone_number,
            password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = user.is_admin
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, phone_number):
        return self.get(phone_number=phone_number)


class UUser(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=9,
                                    validators=[
                                        RegexValidator(regex='^[0-9]*$',
                                                       message='Phone number should be numbers only',
                                                       code='invalid phone number')
                                    ],
                                    unique=True
                                    )

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    # is_active = models.BooleanField(default=False)
    objects = UBaseManager()

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def get_short_name(self):
        return self.phone_number

    class Meta:
        verbose_name = 'User'

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []


class Person(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name='person',
                                on_delete=models.CASCADE,
                                primary_key=True)

    ssn = models.PositiveIntegerField(verbose_name='ssn')
    image = models.ImageField(verbose_name='image', default='image/def_user', upload_to='images/users')
    joined_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.ssn) + " " + UUser(self.user).phone_number

    def delete(self, using=None, keep_parents=False):
        super(Person, self).delete(using=None, keep_parents=False)


class Driver(models.Model):
    driver = models.OneToOneField(Person,
                                  on_delete=models.CASCADE,
                                  primary_key=True,
                                  related_name='driver')

    description = models.TextField(max_length=500, verbose_name="About driver")
    driver_license = models.ImageField(upload_to='licenses/', null=False)
    is_active = models.BooleanField(default=True)
    reg_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return UUser(self.driver.user).phone_number

    def delete(self, using=None, keep_parents=False):
        super(Driver, self).delete(using=None, keep_parents=False)
