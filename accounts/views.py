from django.shortcuts import get_object_or_404, redirect, render
from django.http.response import HttpResponse
from django.contrib import messages, auth


# homepage
def home(request):
    return render(request, 'pages/home.html')

# About
def about(request):
    return render(request, 'pages/about.html')

# Contact
def contact(request):
    return render(request, 'pages/contact.html')

# faq
def faq(request):
    return render(request, 'pages/faq.html')

# Login
def login(request):
    return render(request, 'accounts/login.html')

# Register
def register(request):
    return render(request, 'accounts/register.html')

# Loan
def loan(request):
    return render(request, 'pages/loan.html')

# logout
def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged out.')
    return redirect('login')
