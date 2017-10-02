from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized


class SillyAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        if 'daniel' in request.user.username:
            return True

        return False

    # Optional but recommended
    def get_identifier(self, request):
        return request.user.username


class SillyAuthorization(Authorization):
    def create_list(self, object_list, bundle):
        pass

    def is_authorized(self, request, object=None):
        if request.user.date_joined.year == 2010:
            return True
        else:
            return False

    # Optional but useful for advanced limiting, such as per user.
    def apply_limits(self, request, object_list):
        if request and hasattr(request, 'user'):
            return object_list.filter(author__username=request.user.username)

        return object_list.none()


class UserAuthorization(Authentication):
    def read_list(self, object_list, bundle):
        return object_list.filter(user=bundle.request.user)

    def read_detail(self, object_list, bundle):
        return object_list.obj.user == bundle.obj.user

    def create_list(self, object_list, bundle):
        # Assuming they're auto-assigned to ``user``.
        return object_list

    def create_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def update_list(self, object_list, bundle):
        allowed = []

        # Since they may not all be saved, iterate over them.
        for obj in object_list:
            if obj.user == bundle.request.user:
                allowed.append(obj)

        return allowed

    def update_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def delete_list(self, object_list, bundle):
        # Sorry user, no deletes for you!
        raise Unauthorized("Sorry, no deletes.")

    def delete_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")
