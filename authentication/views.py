from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from . tokens import generate_token
from websiteproject import settings


def home(request):
    return render(request, "authentication/index.html")


def signup(request):
    if request.method == "POST":
        context = {'has_error': False}
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username Already Exists! , Try Again")
            context['has_error'] = True
            # return redirect('home')
            return render(request, 'authentication/signup.html', context, status=409)

        if User.objects.filter(email=email):
            messages.error(request, "Email Already Registered !")
            # return redirect('home')
            context['has_error'] = True
            return render(request, 'authentication/signup.html', context, status=409)

        if len(username) > 10:
            context['has_error'] = True
            messages.error(request, "Username Must Be Under 10 Characters .")

        if pass1 != pass2:
            context['has_error'] = True
            messages.error(request, "Passwords Did Not Match!")

        if not username.isalnum():
            messages.error(request, "Username Must Only Contain Letters & Numbers.")
            context['has_error'] = True
            return redirect('home')


        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        # PRESERVED FOR ADDING A ROUTE TO CONFIRMATION LINK #
        # myuser.is_active = False

        myuser.save()
        messages.success(request, "Your Account Was Created Successfully, We have sent you a confirmation email please confirm in order to activate your account.")

        # TEST EMAIL

        subject = "Welcome To Our Website !"
        message = "Greetings " + myuser.first_name + "! \n" + "Welcome To Our Website \n We Have Sent You A Confirmation Email To Complete Your Registeration ."
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Confirmation Email

        current_site = get_current_site(request)
        email_subject = "Confirm Your Email At Our Website"
        message2 = render_to_string('email_confirmation.html', {
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser),
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()

        return redirect('signin')
    return render(request, "authentication/signup.html")


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "authentication/index.html", {'fname': fname})

        else:
            messages.error(request, "Incorrect Credentials !")
            return redirect('home')

    return render(request, "authentication/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!")
    return redirect('home')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    # PRESERVED FOR ADDING A ROUTE TO CONFIRMATION LINK #

    # if myuser is not None and generate_token.check_token(myuser, token):
    #    myuser.is_active = True
    #    myuser.save()
    #    login(request, myuser)
    #    return redirect('home')
    #else:
    #    return render(request, 'activation_failed.html')


