from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'index.html')

def create_user(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.registration_validator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hashedpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'].lower(),
            password = hashedpw,
        )
        request.session['user_id'] = new_user.id
        return redirect('/')

def login(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.login_validator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        current_user = User.objects.get(email=request.POST['log_email'].lower())
        request.session['user_id'] = current_user.id
        return redirect('/user_page')

def logout(request):
    request.session.flush()
    return redirect('/')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    current_user = User.objects.get(id=request.session['user_id'])
    context = {
        'current_user': current_user,
        'tasks': Task.objects.all(),
    }
    return render(request, 'user_page.html', context)

def create_task(request):
    current_user = User.objects.get(id=request.session['user_id'])
    new_task = Task.objects.create(
        title = request.POST['title'],
        description = request.POST['description'],
        due_date = request.POST['due_date'],
        user = current_user
    )
    return redirect('/user_page')