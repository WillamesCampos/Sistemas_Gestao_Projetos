from uuid import uuid4

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.contrib.auth import get_user_model

from apps.turmas.models import Turma

"""
    Modificando classe User padrão do Django para
    que o username seja o e-mail.
"""

class DjangoCustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class DjangoCustomUser(AbstractBaseUser, PermissionsMixin):

    objects = DjangoCustomUserManager()

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser

    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin


User = get_user_model()


class Usuario(User):
    nome = models.CharField(
        max_length=300
    )
    turma = models.ForeignKey(
        Turma,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )


    class Meta:
        abstract = True


class Aluno(Usuario):
    codigo = models.UUIDField(
        default=uuid4,
        primary_key=True,
        editable=False
    )
    matricula = models.CharField(
        max_length=12,
        unique=True
    )


    class Meta:
        db_table = 'tb_aluno'
        ordering = ['nome']

    def __str__(self):
        return f'{self.matricula}'


class Professor(Usuario):
    codigo = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False
    )

    class Meta:
        db_table = 'tb_professor'
        verbose_name_plural = 'professores'

    def __str__(self):
        return f'{self.codigo}'
