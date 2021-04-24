from django.contrib import admin
from .models import *

# Register your models here.
class CandidateInline(admin.TabularInline):
    model=Candidate
    extra=1

class CategoryAdmin(admin.ModelAdmin):
    inlines = [CandidateInline]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Candidate)
admin.site.register(Vote)