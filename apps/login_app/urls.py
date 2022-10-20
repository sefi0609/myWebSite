from xml.etree.ElementInclude import include
from django.urls import path, include
from . import views

app_name = 'login_app'

# url patterns
urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login_user', views.login_user, name='login_user'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('tasks', include('apps.todo_list_app.urls')),
    path('calendar', include('apps.calendar_app.urls')),
    path('gallery', include('apps.gallery_app.urls')),
]