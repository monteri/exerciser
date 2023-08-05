from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.message, name='event_hook'),
    path('task/', views.get_task, name='task_hook'),
    path('buttons/', views.button_callback, name='button_callback_hook')
]
