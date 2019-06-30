from django.conf import settings
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.core.validators import RegexValidator


# Create your models here.

class UBaseManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, password):
        if not password or not username:
            raise ValueError("you need to set phone number and password ")

        user = self.model(
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            username=username,
            password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = user.is_admin
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username):
        return self.get(username=username)


class UUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=9,
                                validators=[
                                    RegexValidator(regex='^[0-9]*$',
                                                   message='Phone number should be numbers only',
                                                   code='invalid phone number')
                                ],
                                verbose_name='Phone number',
                                unique=True,
                                default='935852415'
                                )

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_created=True, auto_now=True)
    objects = UBaseManager()

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def get_short_name(self):
        return self.username

    def dict(self):
        return {
            'user_name': self.username
        }

    class Meta:
        verbose_name = 'User'

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']


class Person(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name='person',
                                on_delete=models.CASCADE,
                                primary_key=True)

    ssn = models.PositiveIntegerField(verbose_name='SSN', unique=True)
    first_name = models.CharField(max_length=50, verbose_name='First Name', blank=False, default='')
    last_name = models.CharField(max_length=50, verbose_name='Last Name', blank=False, default='')
    email = models.CharField(max_length=50, verbose_name='e-mail', blank=True, default='')
    image = models.ImageField(verbose_name='image', default='image/def_user', upload_to='images/users')
    joined_date = models.DateTimeField(auto_now_add=True)

    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return str(self.ssn) + " " + UUser(self.user).username

    def delete(self, using=None, keep_parents=False):
        super(Person, self).delete(using=None, keep_parents=False)

    def dict(self):
        return {
            'user': self.user.__str__(),
            'ssn': self.ssn,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'image': self.image.__str__(),
            'joined_date': self.joined_date.__str__()
        }


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
        return UUser(self.driver.user).username

    def delete(self, using=None, keep_parents=False):
        super(Driver, self).delete(using=None, keep_parents=False)
