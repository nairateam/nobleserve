from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('teams/', views.teams, name='teams'),
    path('faq/', views.faq, name='faq'),
    path('logout/', views.logout, name='logout'),

    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),

    path('myAccount/', views.myAccount, name='myAccount'),
    path('staffDashboard/', views.staffDashboard, name='staffDashboard'),
    path('customerDashboard/', views.customerDashboard, name='customerDashboard'),

    # service details
    path('Nobleserve Target Savings Plan/', views.ntsp, name='ntsp'),
    path('The Nobleserve Naira Investment/', views.npn, name='npn'),
    path('Lease Financing/', views.lf, name='lf'),
    path('Corporate and Commercial Loans/', views.ccl, name='ccl'),
    path('Personal Loans/', views.pl, name='pl'),

    #blog details 
    path('blogdetails1/', views.blogdetails1, name='blogdetails1'),
    path('blogdetails2/', views.blogdetails2, name='blogdetails2'),
    path('blogdetails3/', views.blogdetails3, name='blogdetails3'),

]
