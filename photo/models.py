from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100, null=False, blank=False)
    user=models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    def __str__(self):
        return self.name


class Photo(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(null=False, blank=False)
    description=models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name='user')

    def __str__(self):
        return self.description

