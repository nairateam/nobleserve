from django.shortcuts import get_object_or_404, redirect, render
from django.http.response import HttpResponse
from django.contrib import messages, auth
from .forms import UserForm
from .models import User, UserProfile
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required, user_passes_test
from .utils import detectUser

from customers.forms import CustomerForm

# Restrict the staff from accessing the customer page


def check_role_staff(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


# Restrict the customer from accessing the staff page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied


@login_required(login_url='login')
def myAccount(request):
    # request.user is the current loggedin user (based on role)
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

# homepage
def home(request):
    return render(request, 'pages/home.html')

# Register
def register(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('myAccount')
    elif request.method == 'POST':
        # store the data and create the user
        form = UserForm(request.POST)
        customer_form = CustomerForm(request.POST, request.FILES)
        if form.is_valid() and customer_form.is_valid:

            # Create the user using create_user method normally
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(
                first_name=first_name, last_name=last_name, username=username, email=email, password=password)
           
            # set user role and make it active for now before activation
            user.role = User.CUSTOMER
            user.is_active = True
            user.save()

            # Get and save customer other details
            customer = customer_form.save(commit=False) #prepare it 
            customer.user = user
            phone_number = customer_form.cleaned_data['phone_number']
            country = customer_form.cleaned_data['country']
            photo = customer_form.cleaned_data['photo']
            customer.save()

            # Send verification email

            messages.success(
                request, 'Your account has been created sucessfully!')
            return redirect('register')
        else:
            print('invalid form')
            print(form.errors)
    else:
        form = UserForm()
        customer_form = CustomerForm()

    context = {
        'form': form,
        'customer_form': customer_form,
    }
    return render(request, 'accounts/register.html', context)


# Login
def login(request):
    # checking that the user is already loggedin
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        #very important so as to enter the role account.
        return redirect('myAccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('myAccount')
        else:
            messages.error(request, 'Invalid login credentials!')
            return redirect('login')
    return render(request, 'accounts/login.html')


@login_required(login_url='login')
@user_passes_test(check_role_staff)
# Staff Dashboard
def staffDashboard(request):
    # get the userprofile of the loggedin user and pass to the template
    profile = get_object_or_404(UserProfile, user=request.user)
    context = {
        'profile': profile,

    }
    return render(request, 'accounts/staffDashboard.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_customer)
# Customer Dashboard
def customerDashboard(request):
     # get the userprofile of the loggedin user and pass to the template
    profile = get_object_or_404(UserProfile, user=request.user)
    context = {
        'profile': profile,

    }
    return render(request, 'accounts/custDashboard.html', context)

# logout


def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged out.')
    return redirect('login')


# Loan
def products(request):
    return render(request, 'pages/products.html')


# About
def about(request):
    return render(request, 'pages/about.html')

# Contact
def contact(request):
    return render(request, 'pages/contact.html')

# faq
def faq(request):
    return render(request, 'pages/faq.html')

# BLog
def blog(request):
    return render(request, 'pages/blog.html')

#blog Details
def blogdetails1(request):
    return render(request, 'pages/blogdetails/blogpost1.html')

def blogdetails2(request):
    return render(request, 'pages/blogdetails/blogpost2.html')

def blogdetails3(request):
    return render(request, 'pages/blogdetails/blogpost3.html')

#services details page
def ntsp(request):
    return render(request, 'pages/services/ntsp.html')

def npn(request):
    return render(request, 'pages/services/npn.html')

def lf(request):
    return render(request, 'pages/services/leasefinancing.html')

def ccl(request):
    return render(request, 'pages/services/ccl.html')

def pl(request):
    return render(request, 'pages/services/personalloans.html')


def teams(request):
    return render(request, 'pages/teams.html')