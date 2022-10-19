from django.urls import path
from . import views


# url patterns
urlpatterns = [
    path('', views.gallery, name='gallery'),
    path('photo/<str:pk>/', views.viewPhoto, name='photo'),
    path('add/', views.addPhoto, name='add'),
    path('event/<int:pk>/delete/', views.PhotoDelete.as_view(), name='photo-delete'),
]
