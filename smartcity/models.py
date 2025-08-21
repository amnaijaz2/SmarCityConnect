from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.urls import reverse
from django.utils import timezone

# Create your models here.

class ServiceProviderR(models.Model):
    SERVICE_CHOICES = [
        ('plumber', 'Plumber'),
        ('electrician', 'Electrician'),
        ('carpenter', 'Carpenter'),
        ('painter', 'Painter'),
        ('welder', 'Welder'),
        ('cable', 'Cable Provider'),
        ('internet', 'Internet Service'),
        ('groceries', 'Groceries'),
    ]
    
    
    username=models.CharField(max_length=100)
    service_image = models.ImageField(upload_to='service_images/')
    servicename = models.CharField(max_length=100, null=False ,choices=SERVICE_CHOICES)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    Phoneno = models.CharField(max_length=11)
    address = models.TextField()
    email=models.EmailField()
    password = models.CharField(max_length=128, null=False)
    is_approved = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    description = models.TextField(blank=True, null=True)
    is_rejected = models.BooleanField(default=False)
    
    approval_date = models.DateTimeField(null=True, blank=True)

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_is_approved = self.is_approved  # Track approval status changes
    

    def __str__(self):
        return f"{self.username} - {self.get_servicename_display()}"

    def get_absolute_url(self):
        return reverse('service_provider_dashboard')

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    class Meta:
        verbose_name = "Service Provider"
        verbose_name_plural = "Service Providers"
        ordering = ['-id']
class CustomerR(models.Model):
   
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.EmailField()
    password = models.CharField(max_length=128, null=False)
    username = models.CharField(max_length=50,unique=True)
    
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    
    
# Add these models to your existing models.py without changing anything else

class ActivityLog(models.Model):
    ACTIVITY_TYPES = (
        ('provider_registered', 'Provider Registered'),
        ('provider_approved', 'Provider Approved'),
        ('new_customer', 'New Customer'),
        ('new_rating', 'New Rating'),
        ('service_request', 'Service Request'),
        ('profile_update', 'Profile Update'),
    )
    
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPES)
    message = models.TextField()
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)
    related_provider = models.ForeignKey(ServiceProviderR, null=True, blank=True, on_delete=models.SET_NULL)
    related_customer = models.ForeignKey(CustomerR, null=True, blank=True, on_delete=models.SET_NULL)
    
    def get_icon(self):
        icons = {
            'provider_registered': 'user-plus',
            'provider_approved': 'check-circle',
            'new_customer': 'user',
            'new_rating': 'star',
            'service_request': 'tools',
            'profile_update': 'user-edit',
        }
        return icons.get(self.activity_type, 'info-circle')
    
    def get_icon_class(self):
        classes = {
            'provider_registered': 'text-primary',
            'provider_approved': 'text-success',
            'new_customer': 'text-info',
            'new_rating': 'text-warning',
            'service_request': 'text-secondary',
            'profile_update': 'text-dark',
        }
        return classes.get(self.activity_type, 'text-muted')
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Activity Log'
        verbose_name_plural = 'Activity Logs'
    
    def __str__(self):
        return f"{self.get_activity_type_display()} - {self.timestamp}"

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('approval', 'Approval Update'),
        ('rating', 'New Rating'),
        ('message', 'New Message'),
        ('system', 'System Notification'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=100)
    message = models.TextField()
    link = models.CharField(max_length=200, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"