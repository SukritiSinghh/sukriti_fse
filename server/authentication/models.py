from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password

class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=50, unique=True)
    address = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Generate a unique code if not provided
        if not self.code:
            import uuid
            self.code = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'
        db_table = 'authentication_organization'


class Role(models.Model):
    """Defines roles within an organization."""
    ROLE_CHOICES = [
        ('Admin', 'Administrator'),
        ('Manager', 'Manager'),
        ('Employee', 'Employee'),
        ('Finance', 'Finance Professional'),
    ]
    
    name = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()

    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
        db_table = 'authentication_role'


class User(AbstractUser):
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def save(self, *args, **kwargs):
        if self._state.adding and self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'authentication_user'
