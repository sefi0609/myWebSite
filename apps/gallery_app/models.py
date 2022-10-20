from django.db import models
from django.contrib.auth.models import User

# Category model - create a table of category object
class Category(models.Model):
    # Each user have is own categories
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False, blank=False)
    
    def __str__(self):
        return self.name

# Photo model - create a table of photo object
class Photo(models.Model):
    # Category is a foreign key, so each user have is own categories and photos
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(null=False, blank=False)
    discription = models.TextField()

    def __str__(self):
        return self.discription
