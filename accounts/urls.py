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

    path('myAccount/', views.myAccount, name='myAccount'),
    path('staffDashboard/', views.staffDashboard, name='staffDashboard'),
    path('customerDashboard/', views.customerDashboard, name='customerDashboard'),

    # service details
    path('Nobleserve Target Savings Plan/', views.ntsp, name='ntsp'),
    path('Nobleserve Promissory Notes/', views.npn, name='npn'),
    path('Lease Financing/', views.lf, name='lf'),
    path('Corporate and Commercial Loans/', views.ccl, name='ccl'),
    path('Personal Loans/', views.pl, name='pl'),

]
