from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.utils import timezone
from django.core.exceptions import ValidationError



class Task(models.Model):
    content = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    priority = models.IntegerField(default=2, validators=[MinValueValidator(1), MaxValueValidator(10)])
    dateStart = models.DateTimeField(models.DateTimeField(default=timezone.now))
    dateFinish = models.DateTimeField(models.DateTimeField(default=timezone.now))

    def __str__(self):
        return f'{self.content}'


    class Meta:
        ordering = ['-date_created']
