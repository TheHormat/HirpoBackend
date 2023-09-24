# from django.db.models import Q

# from django.contrib.auth import get_user_model

# MyUser = get_user_model()

# class UsernameOrEmailBackend(object):
#     def authenticate(self, username=None, password=None, **kwargs):
#         try:
#             user = MyUser.objects.get(Q(username=username)|Q(email=username))
#             if user.check_password(password):
#                 return user
#         except MyUser.DoesNotExist:
#             return None