from django.db import models
from django.contrib.auth.models import User
from .utils import image_resize
# Create your models here.


LEVELS = (
    ('100 Level', '100 Level'),
    ('200 Level', '200 Level'),
    ('300 Level', '300 Level'),
    ('400 Level', '400 Level'),
    ('500 Level', '500 Level')
)

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural="Categories"
        ordering = ['name']
    

class Candidate(models.Model):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    level = models.CharField(max_length=100, choices=LEVELS)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    cover = models.ImageField(upload_to="candidates")
    def __str__(self):
        return f"{self.get_full_name()} -{self.category}"
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    def get_votes(self):
        return self.vote_set.all()
    def is_winner(self):
        winner_votes = self.get_votes()
        verdict = True
        for candidate in self.category.candidate_set.all():
            votes = candidate.get_votes()
            if votes > winner_votes:
                verdict = False
            # else:
            #     verdict = False
        return verdict

    def save(self, *args, **kwargs):
        image_resize(self.cover, 1000,1000)
        super().save(*args, **kwargs)

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user} - {self.candidate}"
    