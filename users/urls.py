from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.user_list, name='user-list'),
    path('users/<uuid:user_id>/', views.user_detail, name='user-detail'),
]