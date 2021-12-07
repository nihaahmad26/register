from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def reg_validator(self, data):
        errors=()
        if len(data['first_name']) < 2:
            errors['first_name'] = "First name should be at least 2 characters"
        if len(data['last_name']) < 2:
            errors['last_name'] = "Last name should be at least 2 characters long"
    
        if len(data['email']) == 0:
            errors['email'] = "Please enter an email"
        
        elif not EMAIL_REGEX.match(data['email']):
            errors['email'] = "Please enter valid email"

        all_users = User.objects.filter(email = data['email'])
        
        if len(all_users) > 0:
            errors['duplicate'] = "Email is taken"
        
        if len(data['password']) < 8:
            errors['password'] = "Password must be atleast 8 characters long"
        if data['password'] != data['confirm']:
            errors["unmatch"] = "passwords do not match"
        return errors
    
    def login_validator(self, data):
        errors = ()
        existing = User.objects.filter(email = data['email'])
        if len(data['email']) == 0:
            errors['email'] = "must enter email"
        if len(data['password']) == 0:
            errors['password'] = "must enter password" 
        elif bcrypt.checkpw(data['password'].encode(), existing[0].password.encode()) != True:
            errors['password'] = "email and password do not match"

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    objects = UserManager()
