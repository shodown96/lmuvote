from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from polls.forms import SignUpForm
from django.contrib import messages
from django.conf import settings
import datetime, requests, random
from requests.exceptions import ConnectionError

from django.core.paginator import Paginator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .serializers import *
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated

DEADLINE = settings.DEADLINE
TODAY = datetime.datetime.today()
WEBSITE_EMAIL = settings.WEBSITE_EMAIL
RECIEVER_EMAIL = settings.RECIEVER_EMAIL


def is_valid(param):
    return param != "" and param is not None

def test_reg_no(reg_no: str):
    url = f"https://att.lmu.edu.ng/assets/passports/{reg_no}.JPG"
    try:
        r = requests.get(url)
        print(r.status_code == 200)
        return r.status_code == 200
    except ConnectionError as e:
        print("Connection Error")
        return False

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening
    
# AUTHENTICATION
def signup(request):
    if TODAY < DEADLINE:
        form = SignUpForm()
        if request.POST:
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                password = User.objects.make_random_password(15)
                user.set_password(password)
                if test_reg_no(form.cleaned_data['reg_no']):
                    user.save()
                    print(form.cleaned_data['reg_no'])
                    print(password)
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


# NORMAL VIEWS
class CategoryListView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class Deadline(APIView):
    return  Response({"deadline":DEADLINE}, status=status.HTTP_200_OK)

class CategoryDetailView(RetrieveAPIView):
    serializer_class = CategoryDetailSerializer
    queryset = Category.objects.all()

class CandidateListView(ListAPIView):
    serializer_class = CandidateSerializer
    queryset = Candidate.objects.all()

    def get_queryset(self):
        category = self.request.query_params.get('category', "")
        q = Candidate.objects.all()
        if is_valid(category):
            q = Candidate.objects.filter(category=category)
        return q

class VoteAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VoteSerializer
    
    def post(self, request, *args, **kwargs):
        if TODAY<DEADLINE:
            serializer = self.serializer_class
            # serializer.is_valid(raise_exception=True)
            message = ""
            
            if serializer.is_valid():
                vote = serializer.save(commit=False)
                vote.user = request.user
                old_vote = Vote.objects.filter(user=request.user, category=vote.category)
                if old_vote.exists():
                    message = "You have already voted for this category, thank you"
                    return Response({'message':message, status=status.HTTP_200_OK})
                else:
                    vote.save()
                    message = "Voting Successful"
                    # last = request.POST.get("last")
                    # page = int(request.POST.get("page"))
                    return Response({'message':message, status=status.HTTP_200_OK})
                    # if last:
                    #     message = "Thank you for your votes"
                    #     return
                    # else:
                    #     page += 1
                    #     return redirect("/category/?page="+str(page))
            else:
                message = serializer.errors
            return Response({'message':message, status=status.HTTP_400_BAD_REQUEST})
            message = "Ino dey work like that bruff"
            return Response({'message':message, status=status.HTTP_403_FORBIDDEN})
        else:
            message = "Deadline, bruhh"
            return Response({'message':message, status=status.HTTP_403_FORBIDDEN})
        return Response({'message':message, status=status.HTTP_200_OK})

@login_required
def vote(request):
    if TODAY<DEADLINE:
        if request.POST:
            form = VoteForm(request.POST)
            if form.is_valid():
                vote = form.save(commit=False)
                vote.user=request.user
                old_vote = Vote.objects.filter(user=request.user, category=vote.category)
                if old_vote.exists():
                    messages.error(request, "You have already voted for this category, thank you", "danger")
                    return redirect(request.META['HTTP_REFERER'])
                else:
                    vote.save()
                    messages.success(request, "Voting Successful")
                    last = request.POST.get("last")
                    page = int(request.POST.get("page"))
                    if last:
                        messages.info(request, "Thank you for your votes")
                        return redirect("polls:categories")
                    else:
                        page += 1
                        return redirect("/category/?page="+str(page))
            else:
                messages.error(request, form.errors, "danger")
                return redirect(request.META['HTTP_REFERER'])
            messages.error(request, "Ino dey work like that bruff", "danger")
            return redirect(request.META['HTTP_REFERER'])
    else:
        messages.error(request, "Deadline, bruhh", "danger")
        return redirect(request.META['HTTP_REFERER'])

class ResultsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VoteSerializer
    def post(self, request, *args, **kwargs):
        if TODAY >= DEADLINE:
            data = []
            for category in Category.objects.filter(c_type="Candidate"):
                dataset = {
                    'category':category.name,
                    'labels':[],
                    'votes':[],
                    'bgColor':[],
                    'bColor':[]
                }
                for candidate in category.candidate_set.all():
                    votes = candidate.vote_set.filter(category=category).count()
                    color = str(random.choices(range(255), k=3)).strip("[]")
                    dataset['labels'].append(candidate.get_full_name())
                    dataset['votes'].append(votes)
                    dataset['bgColor'].append(f"rgb({color})")
                    dataset['bColor'].append(f"rgb({color})")
                data.append(dataset)
            context = {
                'categories': Category.objects.filter(c_type="Candidate"),
                'data':data
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            return Response({"message":"Chills chills, countdown still on"}, status=status.HTTP_400_BAD_REQUEST)

class ContactAPIView(APIView):
    # authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, *args, **kwargs):
        serializer = ContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        content = serializer.data
        current_site = get_current_site(self.request)
        content['domain'] = current_site.domain
        content['protocol'] = PROTOCOL
        email = EmailMessage(
            subject="Contact",
            body= render_to_string("polls/email.txt", content),
            from_email=WEBSITE_EMAIL,
            to=[RECIEVER_EMAIL,]
        )
        email.send()
        return Response({"message":"sent"}, status=status.HTTP_200_OK)

# context = {
# 'name' : form.cleaned_data['name'],
# 'email' : form.cleaned_data['email'],
# 'content' : form.cleaned_data['content'],
# }
# content = render_to_string("polls/email.txt", context)
# email = EmailMessage(
#     'New Contact form email',
#     content,
#     WEBSITE_EMAIL,
#     [RECIEVER_EMAIL,],
#     headers={'Message-ID': make_msgid(), 'Reply to':context['email']},
# )