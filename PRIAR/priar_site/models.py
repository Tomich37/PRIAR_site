from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, login, password=None, email=None):
        if not login:
            raise ValueError('The Login field must be set')
        
        if not password:
            raise ValueError('The Password field must be set')

        user = self.model(login=login, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password, email=None):
        user = self.create_user(login, password, email)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class UsersModel(AbstractBaseUser, PermissionsMixin):
    login = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=128)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['password']

    # Используем related_name для обратных связей с группами и разрешениями
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to.'),
        related_name='users_groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='users_permissions'
    )

    def __str__(self):
        return self.login
    
    class Meta:
        app_label = 'priar_site'
        db_table = 'users'
