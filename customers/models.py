from django.db import models
from accounts.models import User, UserProfile
from shortuuid.django_fields import ShortUUIDField
from django.db.models.fields.related import ForeignKey, OneToOneField

# Create your models here.


class PersonalLoan(models.Model):

    # jobstatus- value and key
    transaction_status_choices = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Declined', 'Declined'),
        ('Paid', 'Paid'),
    )

    # gender
    sex_choices = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

# in django we dont need to define the primary key it happens automatically behind the scene
    transaction_id = ShortUUIDField(
        length=12,
        max_length=40,
        prefix="NBL_",
        alphabet="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-",

    )

    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE) #customer name
    sex = models.CharField(choices=sex_choices, max_length=100)
    dob = models.DateField(max_length=8)
    address = models.CharField(max_length=250)
    occupation = models.CharField(max_length=100)
    purpose_of_loan = models.TextField(max_length=100)
    status = models.CharField(
        choices=transaction_status_choices, max_length=100)
    amount = models.CharField(max_length=10)
    duration = models.DateField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # solves the issue with nontype
        return self.sex


class TargetSaving(models.Model):

    # targetSavings- value and key
    transaction_status_choices = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Declined', 'Declined'),
        ('Paid', 'Paid'),
    )


# in django we dont need to define the primary key it happens automatically behind the scene
    transaction_id = ShortUUIDField(
        length=12,
        max_length=40,
        prefix="NBL_",
        alphabet="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+!#,~-%&*£",

    )

    user = models.OneToOneField(
        User, related_name='tuser', on_delete=models.CASCADE)
    # they can always add more fields to their profile later on.
    fullname = models.CharField(max_length=250, blank=True, null=True)
    user_profile = models.OneToOneField(
        UserProfile, related_name='tuserprofile', on_delete=models.CASCADE)
    amount = models.CharField(max_length=10)
    start_save = models.DateField(max_length=8)
    save_by = models.DateField(max_length=8)
    status = models.CharField(
        choices=transaction_status_choices, max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # solves the issue with nontype
        return self.fullname or ''
