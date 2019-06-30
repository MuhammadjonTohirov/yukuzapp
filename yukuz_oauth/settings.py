from django.conf import settings
from django.contrib.auth.hashers import check_password
from yukuz_oauth.models import UUser


class SettingsBackend:
    """
    Authenticate against the settings ADMIN_LOGIN and ADMIN_PASSWORD.

    Use the login name and a hash of the password. For example:

    ADMIN_LOGIN = 'admin'
    ADMIN_PASSWORD = 'pbkdf2_sha256$30000$Vo0VlMnkR4Bk$qEvtdyZRWTcOsCnI/oQ7fVOu1XAURIZYoOZ3iq8Dr4M='
    """

    def authenticate(self, request, phone_number=None, password=None):
        login_valid = (settings.ADMIN_LOGIN == phone_number)
        pwd_valid = check_password(password, settings.ADMIN_PASSWORD)
        if login_valid and pwd_valid:
            try:
                user = UUser.objects.get(phone_number=phone_number)
            except UUser.DoesNotExist:
                # Create a new user. There's no need to set a password
                # because only the password from settings.py is checked.
                user = UUser(phone_number=phone_number)
                user.is_staff = True
                user.is_superuser = True
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return UUser.objects.get(pk=user_id)
        except UUser.DoesNotExist:
            return None

    def has_perm(self, user_obj, perm, obj=None):
        return user_obj.phone_number == settings.ADMIN_LOGIN
