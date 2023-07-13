from django.urls import path, include
from . import views

urlpatterns = [
    #products
    path('personalloan/add/', views.addpersonalloan, name='addpersonalloan'),
    path('personalloan/view/', views.viewpersonalloan, name='viewpersonalloan'),

]
