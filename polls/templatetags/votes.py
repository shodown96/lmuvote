from django import template
from django.conf import settings
from ..models import Category
import datetime

DEADLINE = settings.DEADLINE
TODAY = datetime.datetime.today()

register = template.Library()

@register.simple_tag
def candidate_votes(votes, category):
    return votes.filter(category=category).count()

@register.simple_tag
def winner(winner_candidate,category):
    winner_votes = candidate_votes(votes=winner_candidate.vote_set.all(), category=category)
    verdict = True

    for candidate in category.candidate_set.all():
        votes = candidate_votes(votes=candidate.vote_set.all(), category=category)
        if votes > winner_votes:
            verdict = False
        # else:
        #     verdict = False
    return verdict

@register.simple_tag
def today():
    return TODAY

@register.simple_tag
def deadline():
    return DEADLINE

@register.simple_tag
def deadline_isoformat():
    return DEADLINE.isoformat()

@register.filter
def increment(count):
    return count+1

@register.simple_tag
def ccategories():
    return Category.objects.all()