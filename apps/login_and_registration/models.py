
from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
class UserManager(models.Manager):
    def isValid(self, form_data):
        print "Inside isValid method."
        valid = True
        errors = []

        if len(form_data['first_name'])<2 or len(form_data['last_name'])<2:
            errors.append("First and last name must be at least 2 characters long.")
            valid=False
        if not NAME_REGEX.match(form_data['first_name']) or not NAME_REGEX.match(form_data['last_name']):
            valid=False
            errors.append("Please enter a name using letters only.")
        if not EMAIL_REGEX.match(form_data['email']):
            valid=False
            errors.append("Please enter a valid email address.")
        if User.objects.filter(email = form_data['email']).first():
            valid=False
            errors.append("That email is already taken.")
        if len(form_data['password'])<8:
            valid=False
            errors.append("Password must be at least 8 characters.")
        if str(form_data['password']) != str(form_data['password_confirmation']):
            valid=False
            errors.append("Password confirmation does not match password.")
        return {"pass": valid, "errors": errors}

    def logging_in(self, form_data):
        errors = []
        valid = True
        if User.objects.filter(email = form_data['email']).first() == None:
            errors.append("That email does not exist")
            valid=False
        elif User.objects.filter(password = form_data['password']).first() == None:
            errors.append('Invalid password')
            valid=False
        return {"pass": valid, "errors": errors}



class User(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.CharField(max_length=25)
    password = models.CharField(max_length=25)
    password_confirmation = models.CharField(max_length=25)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    objects = UserManager()
