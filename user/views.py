from django.shortcuts import render
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import redirect
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        print(username,password)

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'user/login.html')

def signup(request):
    if(request.method == 'POST'):
        # username = request.POST['username']
        # email = request.POST['email']
        # phone = request.POST['phone']
        # password = request.POST['password']
        # cpassword = request.POST['confirm_password']

        form = RegistrationForm(request.POST)

        if form.is_valid():
            try:
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                phone = form.cleaned_data['phone']
                password = form.cleaned_data['password']

                print(username,email,phone,password)

                user = User.objects.create_user(username=username, password=password,email=email)
                user.phone = phone
                
                print(user)
                user.save()
                messages.success(request, 'You are now registered and can log in')
                return redirect('login')
            except:
                messages.error(request, 'Already exists username or email')
                return redirect('signup')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')
    else:
      form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'user/register.html',context)
    # if password == cpassword:
    #     if User.objects.filter(username=username).exists():
    #         messages.error(request, 'That username is taken')
    #         return redirect('signup')
    #     else:
    #         if User.objects.filter(email=email).exists():
    #             messages.error(request, 'That email is being used')
    #             return redirect('signup')
    #         else:
    #             user = User.objects.create_user(username=username, password=password,email=email)
    #             user.save()
    #             messages.success(request, 'You are now registered and can log in')
    #             return redirect('login')
    # else:
    #     messages.error(request, 'Passwords do not match')
    #     return redirect('signup')
   

def settings(request):
    if(request.method == 'POST'):
        print(request.POST)
        name = request.POST['name']
        password = request.POST['password']
        email = request.POST['email']
        phone = request.POST['phone']
        gender = request.POST['gender']
        print(name,password)    
    return render(request, 'user/settings.html')





@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')