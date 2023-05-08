from django.shortcuts import render ,get_object_or_404
from django.contrib import messages, auth
# from django.contrib.auth.models import User
from .models import User,UserProfile
from checkout.models import Order, OrderProduct

from django.shortcuts import redirect
from .forms import RegistrationForm, UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login


# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from cart.views import _cart_id
from cart.models import Cart,CartItem

from decouple import config

import sendgrid
from sendgrid.helpers.mail import Mail, Email, To
import requests
from django.conf import settings



def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user is not None:
            try:    
               cart = Cart.objects.get(cart_id=_cart_id(request))
               is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
               if is_cart_item_exists:
                     cart_item = CartItem.objects.filter(cart=cart)
                     # Getting the product variations by cart id
                     product_variation = []
                     for item in cart_item:
                          variation = item.variations.all()
                          product_variation.append(list(variation))
                     

                     cart_item = CartItem.objects.filter(user=user)
                     ex_var_list = []
                     id = []
                     for item in cart_item:
                          existing_variation = item.variations.all()
                          ex_var_list.append(list(existing_variation))
                          id.append(item.id)
                     
                     for pr in product_variation:
                          if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                          else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                 item.user = user
                                 item.save()
            except:
                print("Cart error in login view")
                pass
            auth_login(request, user)
            messages.success(request, 'You are now logged in')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                # next=/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'user/login.html')

def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']

            user = User.objects.create_user(name=name,email=email,username=username, password=password)
            user.phone = phone
            user.save()


            # Create a user profile
            profile = UserProfile()
            profile.user_id = user.id
            profile.profile_picture = 'assets/images/user/user-profile.png'
            profile.save()

            
            # Send email
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('user/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })


            from_email = Email(config('FROM_EMAIL'))
            to_email = To(email)
            subject = mail_subject

            
            content = Mail(from_email, to_email, subject, message)
            sg = sendgrid.SendGridAPIClient(api_key=config('EMAIL_HOST_PASSWORD'))
            
            sg.send(content)

            messages.success(request, 'You are now registered. Please verify your email address.')
            return redirect('/login/?command=verification&email='+email)

            return redirect('login')
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
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('settings')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'user/settings.html',context)






@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
        print(user,token,uidb64,uid)
        print("try block")
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    print(user)
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('signup')
    


def forgotPassword(request):
    if(request.method == 'POST'):      
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            current_site = get_current_site(request)
            mail_subject = 'Reset your password.'
            message = render_to_string('user/reset_password_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            
            from_email = Email(config('FROM_EMAIL'))
            to_email = To(email)
            subject = mail_subject

            
            content = Mail(from_email, to_email, subject, message)
            sg = sendgrid.SendGridAPIClient(api_key=config('EMAIL_HOST_PASSWORD'))
            
            sg.send(content)

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')

    return render(request, 'user/forgot_password.html')



def resetPassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
        print(user,token,uidb64,uid)
        print("try block")
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    print(user)
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request,'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link expired Invalid activation link')
        return redirect('login')
    

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        cpassword = request.POST['confirm_password']
        if password == cpassword:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful.')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('resetPassword')
    else:
        return render(request, 'user/resetPassword.html')
    





# @login_required(login_url = 'login')
# def dashboard(request):
#     orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
#     orders_count = orders.count()

#     userprofile = UserProfile.objects.get(user_id=request.user.id)
#     context = {
#         'orders_count': orders_count,
#         'userprofile': userprofile,
#     }
#     return render(request, 'accounts/dashboard.html', context)


