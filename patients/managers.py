# from django.contrib.auth.base_user import BaseUserManager
# from django.utils.translation import gettext_lazy as _


# class PatientManager(BaseUserManager):

#     def create_user(self, email, password):
        
#         if not email:
#             raise ValueError(_("The Email must be set"))
        
#         user = self.model(
#                 email=self.normalize_email(email),
#             )
#         user.set_password(password)
#         user.save()
#         return user

#     def create_superuser(self, email, password):
        
#         user = self.create_user(
#                 email=self.normalize_email(email),
#                 password=password
#             )
        
#         user.is_staff=True
#         user.is_superuser=True
#         user.is_active=True
        
#         user.save()
        
#         return user