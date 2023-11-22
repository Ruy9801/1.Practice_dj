from django.db import models
from django.contrib.auth.base_user import BaseUserManager 
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.hashers import make_password

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **kwargs):
        if not email:
            return ValueError('Email is required')
        email = self.normalize_email(email=email)
        user = self.model(email=email, **kwargs)
        user.create_activation_code()
        user.password = make_password(password)
        user.save()
        return user 
    
    def create_user(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)
        return self._create_user(email, password, **kwargs)
    
    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)
        return self._create_user(email, password, **kwargs)
    
    def create_author(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', False)
        return self._create_user(email, password, **kwargs)

    

class Customer(AbstractUser):
    phone_number = models.CharField(max_length=25, unique=False)
    email = models.EmailField(unique=False)
    password = models.CharField(max_length=150)
    username = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='cust_avatars/', blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=100, blank=True)

    first_name = None 
    last_name = None 
    groups = models.ManyToManyField(
        Group,
        related_name='customer_users',
        blank=True, 
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customer_user',
        blank=True,
        verbose_name='user permissions',
        error_messages={
            'add': 'You cannot add permission directly to users.',
            'remove': 'You cannot remove permission directly from users.',
        },
    )

    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return f'{self.username} --> {self.balance}'
    
    def create_activation_code(self):
        import uuid 
        code = str(uuid.uuid4())
        self.activation_code = code

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'


class Author(AbstractUser):
    phone_number = models.CharField(max_length=25, unique=False)
    email = models.EmailField(unique=False)
    password = models.CharField(max_length=150)
    author = models.BooleanField(default=True)
    username = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='auth_avatars/', blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=100, blank=True)

    first_name = None
    last_name = None 
    groups = models.ManyToManyField(
        Group,
        related_name='author_users',
        blank=True, 
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='author_user',
        blank=True,
        verbose_name='user permissions',
        error_messages={
            'add': 'You cannot add permission directly to users.',
            'remove': 'You cannot remove permission directly from users.',
        },
    )

    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return f'{self.username} --> {self.balance}'
    
    def create_activation_code(self):
        import uuid 
        code = str(uuid.uuid4())
        self.activation_code = code

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'