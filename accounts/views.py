from django.shortcuts import get_object_or_404, redirect, render
from django.http.response import HttpResponse
from django.contrib import messages, auth
from .forms import UserForm
from .models import User, UserProfile
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required, user_passes_test
from .utils import detectUser
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from customers.forms import CustomerForm, PersonalLoanForm, TargetSavingsForm, PerformApprovalLoanForm

from customers.forms import CustomerForm
from customers.models import PersonalLoan, TargetSaving
from django.db.models import Q
from .filters import PersonalLoanFilter
from django.urls import reverse
import json
from django.views.decorators.http import require_POST


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
            customer = customer_form.save(commit=False)  # prepare it
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
        # very important so as to enter the role account.
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

    # query all products total requests and customers
    total_no_of_customers = User.objects.filter(role='2').all().count()
    total_no_of_personal_loans = PersonalLoan.objects.all().count()
    total_no_of_target_savings = TargetSaving.objects.all().count()

    context = {
        'profile': profile,
        'total_no_of_customers': total_no_of_customers,
        'total_no_of_personal_loans': total_no_of_personal_loans,
        'total_no_of_target_savings': total_no_of_target_savings,

    }
    return render(request, 'accounts/staffDashboard.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_staff)
def personalLoans(request):
    # To show loggedin Userprofile -sho is adding job
    profile = get_object_or_404(UserProfile, user=request.user)

    # fetch only customer recent  loan transactions queries
    Personalloans = PersonalLoan.objects.all().order_by('-created_at')
    total_no_of_pl = PersonalLoan.objects.all().count()

    my_Filter = PersonalLoanFilter(request.GET, queryset=Personalloans)
    all_personalLoans = my_Filter.qs

    # paginatingby filter here
    items_per_page = 10
    paginator = Paginator(all_personalLoans, items_per_page)

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'total_no_of_pl': total_no_of_pl,
        'profile': profile,
        "Personalloans": Personalloans,
        "my_Filter": my_Filter,
        "all_personalLoans": all_personalLoans
    }
    return render(request, 'staffs/personal_loans.html', context)


# View Personal LoanDetails
@login_required(login_url='login')
@user_passes_test(check_role_staff)
def personalLoanDetails(request, pk):

    # get a particular loan request detail
    ploan = get_object_or_404(PersonalLoan, pk=pk)

    # Get the profile of the customer
    profile = get_object_or_404(UserProfile, pk=pk)

    form = PersonalLoanForm(request.POST, instance=ploan)
    if form.is_valid():
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "loanListChanged": None,

                })
            }
        )
    context = {
        'form': form,
        'ploan': ploan,
        'profile': profile,
    }
    return render(request, 'staffs/personal_loanDetails.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_staff)
def performApproval(request, pk):

    ploan = get_object_or_404(PersonalLoan, pk=pk)

    # Get the profile of the customer
    profile = get_object_or_404(UserProfile, pk=pk)
    if request.method == "POST":
        form = PerformApprovalLoanForm(request.POST, instance=ploan)
        if form.is_valid():
            form.save()

            response = HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "loanListChanged": None,
                        "showMessage": "Customer's Personal Loan Status was Successfully Updated"
                    })


                })

        response["HX-Redirect"] = reverse("personalLoans")
        return response

    else:
        form = PerformApprovalLoanForm(instance=ploan)
        context = {
            'form': form,
            'ploan': ploan,
            'profile': profile,
        }
    return render(request, 'staffs/perform_approvalform.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_staff)
def confirm_personalloanremoval(request, pk):
    ploan = get_object_or_404(PersonalLoan, pk=pk)

    # Get the profile of the customer
    profile = get_object_or_404(UserProfile, pk=pk)

    if request.method == "POST":
        form = PerformApprovalLoanForm(request.POST, instance=ploan)
        if form.is_valid():

            response = HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "loanListChanged": None,
                    })


                })

        response["HX-Redirect"] = reverse("personalLoans")
        return response

    else:
        form = PerformApprovalLoanForm(instance=ploan)
        context = {
            'form': form,
            'ploan': ploan,
            'profile': profile,
        }
    return render(request, 'staffs/delete_personalloanform.html', context)


@ require_POST
@login_required(login_url='login')
@user_passes_test(check_role_staff)
def remove_personalloan(request, pk):
    ploan = get_object_or_404(PersonalLoan, pk=pk)
    ploan.delete()

    response = HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "movieListChanged": None,
                "showMessage": "Customer's Personal Loan Request Deleted"
            })

        })
    response["HX-Redirect"] = reverse("personalLoans")
    return response


@login_required(login_url='login')
@user_passes_test(check_role_staff)
def targetSavings(request):
    # To show loggedin Userprofile -sho is adding job
    profile = get_object_or_404(UserProfile, user=request.user)

    # fetch only customer recent  loan transactions queries
    Target_savings = TargetSaving.objects.all().order_by('-created_at')
    total_no_of_ts = TargetSaving.objects.all().count()

    my_Filter = PersonalLoanFilter(request.GET, queryset=Target_savings)
    all_targetSavings = my_Filter.qs

    # paginatingby filter here
    items_per_page = 10
    paginator = Paginator(all_targetSavings, items_per_page)

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'total_no_of_ts': total_no_of_ts,
        'profile': profile,
        "Target_savings": Target_savings,
        "my_Filter": my_Filter,
        "all_targetSavings": all_targetSavings,
    }
    return render(request, 'staffs/target_savings.html', context)


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

# blog Details


def blogdetails1(request):
    return render(request, 'pages/blogdetails/blogpost1.html')


def blogdetails2(request):
    return render(request, 'pages/blogdetails/blogpost2.html')


def blogdetails3(request):
    return render(request, 'pages/blogdetails/blogpost3.html')

# services details page


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
