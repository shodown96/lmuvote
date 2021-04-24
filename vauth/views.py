from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from polls.forms import SignUpForm
from django.contrib import messages
from django.conf import settings
import datetime, requests
from requests.exceptions import ConnectionError

DEADLINE = settings.DEADLINE
TODAY = datetime.datetime.today()
WEBSITE_EMAIL = settings.WEBSITE_EMAIL
# https://att.lmu.edu.ng/assets/passports/1800528.JPG
# for idx,item in enumerate(list):

def test_reg_no(reg_no: str):
    url = f"https://att.lmu.edu.ng/assets/passports/{reg_no}.JPG"
    try:
        r = requests.get(url)
        print(r.status_code == 200)
        return r.status_code == 200
    except ConnectionError as e:
        print("Connection Error")
        return False

    
# Create your views here.
def signup(request):
    if TODAY < DEADLINE:
        form = SignUpForm()
        if request.POST:
            form = SignUpForm(request.POST)
            if form.is_valid() and form.check_user():
                user = form.save(commit=False)
                password = User.objects.make_random_password(15)
                user.set_password(password)
                # user.username = f"{user.last_name}.{user.first_name}".lower()
                # user.save() #soladoye.elijah - 4jSmDXwyFzMrRcX
                # print(form.cleaned_data['reg_no'])
                # print(password)
                # user.email_user(
                #     "Registration successfull",
                #     f"Thank you for registering to our website. your username is {user.username} and password is {password}",
                #     WEBSITE_EMAIL
                # )
                # auth_login(request, user)
                # messages.success(request, "Registration successful, please check your webmail")
                # return redirect("polls:categories")

                if test_reg_no(form.cleaned_data['reg_no']):
                    user.save()
                    # print(form.cleaned_data['reg_no'])
                    # print(password)
                    user.email_user(
                        "Registration successfull",
                        f"Thank you for registering to our website. your username is {user.username} and password is {password}",
                        WEBSITE_EMAIL
                    )
                    auth_login(request, user)
                    messages.success(request, "Registration successful")
                    return redirect("polls:categories")
                else:
                    messages.error(request, "Your School credentials are invalid or network issues, please try again later", "danger")
                    return render(request,"registration/signup.html", {'form':form})

            else:
                messages.error(request, form.non_field_errors(), "danger")
        return render(request,"registration/signup.html", {'form':form})
    else:
        messages.error(request, "Deadline, bruhh", "danger")
        return redirect(request.META['HTTP_REFERER'])

def login(request):
    form = AuthenticationForm()
    if request.POST:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'],password=form.cleaned_data['password'])
            if user:
                auth_login(request,user)
                messages.success(request, "Login Successful")
                return redirect("polls:categories")
        else:
            messages.error(request, form.non_field_errors(), "danger")
    return render(request,"registration/login.html", {'form':form})

def logout(request):
    # if request.user.is_authenticated:
    auth_logout(request)
    return redirect("polls:index")
    # else:
    #     messages.error(request, "Bros, hwfa na", "danger")
    #     return redirect("polls:index")
