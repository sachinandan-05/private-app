import uuid
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.views import PasswordChangeForm
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.core.mail import send_mail as django_send_mail
from .models import Profile

User = get_user_model()

# Home Page
def home(request):
    return render(request, 'user/home.html')

# Private LogIn Screen
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=username).first()
        if not user_obj:
            user_obj = User.objects.filter(email=username).first()
        
        if not user_obj:
            messages.error(request, 'Username/Email not found.')
            return redirect(request.META.get('HTTP_REFERER'))
        
        profile_obj = Profile.objects.filter(user=user_obj).first()
        if profile_obj and not profile_obj.is_verified:
            messages.error(request, 'Profile is not verified. Check your mail.')
            return redirect(request.META.get('HTTP_REFERER'))

        user = authenticate(username=user_obj.username, password=password)
        if not user:
            messages.error(request, 'Wrong Password.')
            return redirect('/login/')

        request.session['private_admin'] = user.username
        request.session['private_id'] = user.id
        request.session['login_time'] = datetime.now().timestamp()
        return redirect('/view/')

    return render(request, 'login.html', {"checkcon": 0, "Title": "Private "})

# Send Email Verification For Registration
def create_user(username, email, password, auth_token, check):
    sub_domain = 'private-app'
    site_url = f'http://127.0.0.1:8000/verify/{auth_token}'

    if check == 'register':
        user_obj = User(username=username, email=email)
        user_obj.set_password(password)
        user_obj.save()

        profile_obj = Profile.objects.create(
            user=user_obj,
            auth_token=auth_token,
            is_verified=False
        )
        profile_obj.save()

    subject = 'Verify Your Email'
    message = f'Hi {username}, please use the following link to verify your email: {site_url}'
    try:
        django_send_mail(subject, message, 'your-email@example.com', [email])
    except Exception as e:
        print(f"Failed to send email: {e}")

# Register Page
def register_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        if not email.endswith('@gmail.com'):
            msg = 'Please Enter a Valid Gmail Address.....!'
            return JsonResponse({'status': True, 'exists': 'email_error', 'msg': msg})

        if User.objects.filter(username=username).exists():
            msg = 'Username Already Exists.....!'
            return JsonResponse({'status': True, 'exists': 'existuser', 'msg': msg})

        if User.objects.filter(email=email).exists():
            msg = 'Email Already Exists.....!'
            return JsonResponse({'status': True, 'exists': 'existemail', 'msg': msg})

        auth_token = str(uuid.uuid4())
        try:
            create_user(username, email, password, auth_token, 'register')
        except Exception as e:
            print(f"Failed to create user: {e}")
            return JsonResponse({'status': False, 'msg': 'An error occurred. Please try again.'})

        msg = f'Account Was Created For {username} And Activation Link Was Sent To {email}.....!'
        request.session['msg'] = msg
        return JsonResponse({'status': True, 'exists': 'usercreate', 'u_name': 'username', 'msg': msg})

    if 'userid' in request.session:
        return redirect('/')
    return render(request, 'user/register-1.html', {'cartc': '2'})

# Send Email Verification Page
def token_send(request):
    if 'msg' in request.session:
        msg = request.session.pop('msg')
        messages.success(request, msg)
    return render(request, 'user/token_send.html')

# Check Email Verification
def verify(request, auth_token):
    profile_obj = Profile.objects.filter(auth_token=auth_token).first()
    if not profile_obj:
        return redirect('/register/')

    user_obj = profile_obj.user
    if profile_obj.is_verified:
        request.session['private_admin'] = user_obj.username
        request.session['private_id'] = user_obj.id
        request.session['login_time'] = datetime.now().timestamp()
        return redirect('/view/')

    profile_obj.is_verified = True
    profile_obj.save()

    request.session['private_admin'] = user_obj.username
    request.session['private_id'] = user_obj.id
    request.session['login_time'] = datetime.now().timestamp()
    return redirect('/view/')

# Private LogOut
def logout_private_admin(request):
    request.session.flush()
    return redirect('/')

# Reset Password Page
def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email').lower()

        if not email.endswith('@gmail.com'):
            messages.error(request, 'Please Enter Valid Gmail Address.....!')
            return redirect('/password-reset/')

        user = User.objects.filter(email=email).first()
        if not user:
            messages.error(request, 'Email Not Exists.....!')
            return redirect('/password-reset/')

        profile_obj = Profile.objects.filter(user=user).first()
        auth_token = profile_obj.auth_token if profile_obj else str(uuid.uuid4())

        subject = 'Password Reset'
        message = f'Hi {user.username}, please use the following link to reset your password: http://127.0.0.1:8000/verify/{auth_token}'
        try:
            django_send_mail(subject, message, 'your-email@example.com', [email])
        except Exception as e:
            print(f"Failed to send email: {e}")
            messages.error(request, 'Failed to send reset link. Please try again.')
            return redirect('/password-reset/')

        messages.success(request, f'Password Reset Link Was Sent To {email}.....!')
        return redirect('/password-reset/')

    if 'userid' in request.session:
        return redirect('/')
    return render(request, 'user/password-forget.html', {'cartc': '2'})

# Change Password Page
def change_password(request):
    if 'private_admin' not in request.session:
        messages.error(request, 'Please Login First.')
        return redirect('/login/')

    user = User.objects.get(username=request.session.get('private_admin'))
    if request.method == 'POST':
        form = PasswordChangeForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password Changed Successfully ✔')
            return redirect('/change-password/')
    else:
        form = PasswordChangeForm(user=user)

    return render(request, 'change-password-1.html', {
        'form': form,
        'password_master': 'master',
        'password_active': 'password_master',
    })
