from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password, first_name, last_name, date_of_birth, role=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('User must have an email address'))
        if not first_name:
            raise ValueError(_('User must have a first name'))
        if not last_name:
            raise ValueError(_('User must have a last name'))
        if not date_of_birth:
            raise ValueError(_('User must have a date of birth'))
        if not role:
            role = self.model.base_role
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name,
                          date_of_birth=date_of_birth, role=role, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, first_name, last_name, date_of_birth, role=None, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, first_name, last_name, date_of_birth, role, **extra_fields)

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if self.model.base_role == '__all__':
            return queryset
        return queryset.filter(role=self.model.base_role)

