from django.shortcuts import render,redirect, HttpResponse
from django.http import HttpResponse
from .models import *
import datetime
from django.core.paginator import Paginator
from .forms import VoteForm, ContactForm
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
import datetime
from django.contrib.auth.decorators import login_required
import random
from django.template.loader import render_to_string
from django.core.mail.message import make_msgid

DEADLINE = settings.DEADLINE
TODAY = datetime.datetime.today()
WEBSITE_EMAIL = settings.WEBSITE_EMAIL
RECIEVER_EMAIL = settings.RECIEVER_EMAIL
# Create your views here.
def index(request):
    context = {
        'today':TODAY,
        'deadline':DEADLINE
    }
    return render(request,"polls/index.html", context)

def categories(request):
    context = {
        'categories': Category.objects.all(),
        'today':TODAY,
        'deadline':DEADLINE
    }
    return render(request,"polls/categories.html", context)

@login_required
def category(request):
    cat_list = Category.objects.all()
    page = request.GET.get("page")
    paginator = Paginator(cat_list,1)
    context = {
        'categories': paginator.get_page(page),
        'today':TODAY,
        'deadline':DEADLINE
    }
    return render(request,"polls/category.html", context)

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

@login_required
def results(request):
    if TODAY >= DEADLINE:
        data = []
        for category in Category.objects.all():
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
            'categories': Category.objects.all(),
            'data':data
        }
        return render(request, "polls/results.html", context)
    else:
        messages.error(request,"Chills chills, countdown still on", "danger")
        return redirect("polls:index")

def contact(request):
    form = ContactForm()
    if request.POST:
        form = ContactForm(data=request.POST)
        if form.is_valid():
            context = {
            'name' : form.cleaned_data['name'],
            'email' : form.cleaned_data['email'],
            'content' : form.cleaned_data['content'],
            }
            content = render_to_string("polls/email.txt", context)
            email = EmailMessage(
                'New Contact form email',
                content,
                WEBSITE_EMAIL,
                [RECIEVER_EMAIL,],
                headers={'Message-ID': make_msgid(), 'Reply to':context['email']},
            )
            email.send()
            messages.success(request, "Message sent")
            return redirect('polls:contact')
        else:
            messages.error(request, form.errors, "danger")
    return render(request, 'polls/contact.html', {'form':form})