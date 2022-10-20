from django.contrib import admin
from .models import *

# Register models for the admin site
admin.site.register(Category)
admin.site.register(Photo)
