from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('loan/', views.loan, name='loan'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path('logout/', views.logout, name='logout'),

    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),

    #path('myAccount/', views.myAccount, name='myAccount'),
    #path('staffDashboard/', views.staffDashboard, name='staffDashboard'),
    ##path('agentDashboard/', views.agentDashboard, name='agentDashboard'),
    #path('clientDashboard/', views.clientDashboard, name='clientDashboard'),
]