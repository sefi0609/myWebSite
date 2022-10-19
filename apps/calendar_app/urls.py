from django.urls import path, include
from . import views

# url patterns
urlpatterns = [
    path('', views.CalendarView.as_view(), name='calendar'), 
    path('event/new/', views.new_event, name='event_new'),
    path('event/edit/<int:pk>/', views.EventUpdate.as_view(), name='event_edit'),
    path('event/<int:pk>/delete/', views.EventDelete.as_view(), name='event-delete'),
    ]