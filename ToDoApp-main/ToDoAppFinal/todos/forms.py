from django import forms
from .models import Task
import datetime
from django.forms import DateInput

class TaskForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Добавить новую задачу...'}))
    priority = forms.IntegerField(label='', required=True, widget=forms.NumberInput(attrs={'placeholder': 'Приоритет от 0 до 10'}))
    dateStart = forms.DateTimeField(label='Дата начала', required=True, widget=DateInput(attrs={'type': 'datetime-local'}),
                                     initial=datetime.date.today())
    dateFinish = forms.DateTimeField(label='Дата завершения', required=True, widget=DateInput(attrs={'type': 'datetime-local'}))
    class Meta:
        model = Task
        fields = ['content']


class UpdateTaskForm(forms.ModelForm):
    content = forms.CharField(
        label='Название', widget=forms.TextInput(attrs={}))
    complete = forms.BooleanField(label='Выполнено', required=False)
    priority = forms.IntegerField(label='Приоритет', required=True)
    dateStart = forms.DateTimeField(label='Дата начала', required=True, widget=forms.SelectDateWidget)
    dateFinish = forms.DateTimeField(label='Дата завершения', required=True, widget=forms.SelectDateWidget)

    class Meta:
        model = Task
        fields = '__all__'
