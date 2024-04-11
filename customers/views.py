from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import random
import string
from django.contrib.auth.models import User
from customers . models import Customer


def user_logout(request):
    logout(request)
    return render(request,'login.html')

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def send_otp_email(email, otp):
    subject = 'Verification OTP for Your Account'
    message = f'Your OTP for account verification is: {otp}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    try:
        send_mail(subject, message, email_from, recipient_list)
        return True
    except Exception as e:
        # Handle error in sending email
        print(f"Error sending email: {e}")
        return False



def create_account(request):
    if request.method=='POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phoneno = request.POST.get('phoneno')
        password = request.POST.get('psw')
        confirm_password = request.POST.get('psw-repeat')

        try:
            validate_password(password)
        except ValidationError as e:
            error_message = ', '.join(e.messages)
            messages.error(request, error_message)
            return render(request, 'signup.html')

        if password != confirm_password:
            error_message = 'Passwords do not match.'
            messages.error(request,error_message)
            return render(request, 'signup.html')

        otp = generate_otp()
        request.session['signup_data'] = {
            'username': username,
            'email': email,
            'address': address,
            'phoneno': phoneno,
            'password': password,  # Note: It's better to hash the password before storing it in the session
            'otp': otp,
            }
        send_otp_email(email, otp)
        return redirect('verify_otp')

    return render(request, 'signup.html')           

    #         user = User.objects.create_user(
    #             username = username,
    #             password = password,
    #             email = email
    #             )
    #         customer = Customer.objects.create(
    #             name = username,
    #             user = user,
    #             phoneno = phoneno,
    #             address = address
    #             )
    #         return redirect('login')
    #     except Exception as e:
    #         error_message = "username exists"
    #         messages.error(request, error_message)

    # return render(request,'signup.html')


def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('signup_data', {}).get('otp')


        if entered_otp == stored_otp:
            signup_data = request.session.get('signup_data')
            if signup_data:
                username = signup_data['username']
                email = signup_data['email']
                address = signup_data['address']
                phoneno = signup_data['phoneno']
                password = signup_data['password']

                try:
                    # Create User instance
                    user = User.objects.create_user(
                        username=username,
                        password=password,
                        email=email
                    )

                    # Create Customer instance
                    customer = Customer.objects.create(
                        name=username,
                        user=user,
                        phoneno=phoneno,
                        address=address
                    )

                    # Cleanup session data
                    del request.session['signup_data']

                    messages.success(request, 'Account created successfully. Please login.')
                    return redirect('login')
                except Exception as e:
                    error_message = "Error creating user: " + str(e)
                    messages.error(request, error_message)
                    return redirect('account')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('verify_otp')

    return render(request, 'verify_otp.html')


def customer_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('psw')
        print(email,password)
        user = authenticate(request, username=email, password=password)
        print(user)
        # if user is not None:
        if user:
            if user.is_staff:
                login(request, user)
                return redirect('dash')
            login(request, user)
            return redirect('home')
    return render(request,'login.html')