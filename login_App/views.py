from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt

def index(request):
    return render(request,'index.html')

def register(request):
    if request.method == 'POST':
        errors = User.objects.reg_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(first_name = request.POST['first_name'],last_name = request.POST['last_name'], email = request.POST['email'], password = hashed_pw)
        request.session['user_id'] = new_user.id
        return redirect('/success')
    return redirect('/')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    specific_user = User.objects.filter(id = request.session['user_id'])
    context = { 'user': specific_user[0] }
    return render(request, 'success.html', context)

def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        specific_user = User.objects.filter(email = request.POST['email'])
        request.session['user_id'] = specific_user[0]
        return redirect('/success')
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect ('/')