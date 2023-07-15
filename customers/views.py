from django.shortcuts import get_object_or_404, redirect, render
from django.http.response import HttpResponse
from django.contrib import messages, auth
from accounts.models import User, UserProfile
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.utils import detectUser
from .forms import  CustomerForm,PersonalLoanForm, TargetSavingsForm
from django.http import JsonResponse
from django.db.models import Q
from django.urls import reverse
from .models import PersonalLoan, TargetSaving
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import json

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


def get_customer(request):
    customer = User.objects.get(user=request.user)
    return customer



@login_required(login_url='login')
@user_passes_test(check_role_customer)
def addpersonalloan(request):

    # To show loggedin Userprofile (customer)
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == "POST":
        form = PersonalLoanForm(request.POST)
        if form.is_valid():
            sex= form.cleaned_data['sex']
            dob = form.cleaned_data['dob']
            occupation = form.cleaned_data['occupation']
            address = form.cleaned_data['address']
            purpose_of_loan= form.cleaned_data['purpose_of_loan']
            amount = form.cleaned_data['amount']
            duration= form.cleaned_data['duration']

            loan = form.save(commit=False)  # prepare to store
            #who created the personal loan
            loan.created_by = request.user
            loan.status = 'Pending'  # set loan to be pending
            loan.save()
        
            
        response =HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "loanListChanged": None,
                        "showMessage": "Your loan request was created Successfully and Submitted for Review! Check your Loan Applications to See Status of new Request!",
                    })
     
                    
                })
        
        response["HX-Redirect"] = reverse("viewpersonalloan")
        return response 
            
    else:
        form = PersonalLoanForm()
    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'customers/addpersonal_loan.html', context)



@login_required(login_url='login')
@user_passes_test(check_role_customer)
def viewpersonalloan(request):
     # To show loggedin Userprofile -sho is adding job
    profile = get_object_or_404(UserProfile, user=request.user)

    #fetch only customer recent  loan transactions queries
    Personalloans = PersonalLoan.objects.filter(created_by=request.user).order_by('-created_at')
    total_no_of_pl = PersonalLoan.objects.all().count()

    items_per_page = 10
    paginator = Paginator(Personalloans, items_per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'total_no_of_pl': total_no_of_pl,
        'profile': profile,
        "Personalloans": Personalloans, 
    }
    return render(request, 'customers/viewpersonal_loan.html', context)