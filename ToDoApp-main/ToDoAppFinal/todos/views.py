from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm, UpdateTaskForm
from datetime import date, datetime, timedelta
from django.shortcuts import get_object_or_404
import traceback
import logging


# Представление для отрисовки главной страницы
def start_page(request):

    # получаем из БД все задачи в отсортированном по дате завершения виде. 
    todos = Task.objects.all().order_by('-dateFinish')
    # подсчитываем общее кол-во задач
    count_todos = todos.count()
    # получаем выборку задач завершенных с помощью фильтра
    completed_todo = Task.objects.filter(complete=True)
    # получаем кол-во выполненных задач
    count_completed_todo = completed_todo.count()
    # вычисляем кол-во оставшихся задач
    uncompleted = count_todos - count_completed_todo
    

    # Если был получен post запрос. Т.е. пользователь отправил форму с новой задачей
    if (request.POST):
        # из запроса получаем название задачи
        content = request.POST['content']
        # из запроса получаем приоритет задачи
        priority = request.POST['priority']
        # из запроса устанавливаем статус выполнения 0. Т.е. не выполнена
        complete = 0
        # из запроса получаем дату старта задачи
        dateStart = request.POST['dateStart']
        # из запроса получаем дату завершения задачи
        dateFinish = request.POST['dateFinish']
        # проверка что дата завершения не раньше даты начала
        if(datetime.strptime(dateStart,  "%Y-%m-%dT%H:%M").date() > datetime.strptime(dateFinish, "%Y-%m-%dT%H:%M").date()):
            print('Дата завершения не может быть раньше даты начала')
            # в этом случае проверка нашла ошибку ввода и необходимо вернуть пользователю форму
            form = TaskForm()
            # контекст - переменные для отображания в html шаблоне
            context = {
                    'todos': todos,
                    'count_todos': count_todos,
                    'count_completed_todo': count_completed_todo,
                    'uncompleted': uncompleted,
                    'exception': 'Дата завершения не может быть раньше даты начала',
                    }
            # отрисовка шаблона index.index и передача контекста переменных
            return render(request, 'todos/index.html', context)
        else:
            # Дата завершения корректна, то сохраняем новую задачу в БД
            Task.objects.create(content=content, priority=priority, complete = complete, dateStart= dateStart, dateFinish=dateFinish )
        
         # Отрисовываем страницу, возвращаемся на корень сайта
        return redirect('/')
    else:
        # Пользователь не отправил post запрос и ему необходимо отобразить контент страницы
        # получает объект модели данных Task
        form = TaskForm()
        # контекст - переменные для отображания в html шаблоне
        for i, c in enumerate(todos):
            print("dateFinish ", c.dateFinish)
            #2022-12-24 13:38:00+00:00 формат входной даты
            d = datetime.strptime(str(c.dateFinish),  "%Y-%m-%d %H:%M:%S+00:00")

            # конвертированная дата в формат %Y-%m-%d
            d = d.date()
            print(d.isoformat())
            c.dateFinish = d.isoformat()
        

        context = {
                    'todos': todos,
                    'form': form,
                    'count_todos': count_todos,
                    'count_completed_todo': count_completed_todo,
                    'uncompleted': uncompleted,
                    }
         # отрисовка шаблона index.index и передача контекста переменных
        return render(request, 'todos/index.html', context)



# представление для редаткирования информации о задаче по ИД
def update(request, pk):
    # получаем задачу по Id из БД
    task = Task.objects.get(id=pk)

    # получаем весь список задач для вывода статистики
    todos = Task.objects.all() 
    count_todos = todos.count() # определяем кол-во всех задач
    # получаем выборку задач завершенных с помощью фильтра
    completed_todo = Task.objects.filter(complete=True) 
    count_completed_todo = completed_todo.count() # кол-во завершенных задач
    uncompleted = count_todos - count_completed_todo # вычисляем кол-во незавершенных задач
    
    # Если был получен post запрос. Т.е. пользователь отправил форму с новой задачей
    if request.method == 'POST':
        # получаем данные с отправленной пользователем формы
        form = UpdateTaskForm(request.POST, instance=task)
        if form.is_valid(): # проверка, что форма целая
            try:
                 # проверка что дата завершения не раньше даты начала
                if(int(form.data.get('dateFinish_year')) <= int(form.data.get('dateStart_year')) and int(form.data.get('dateFinish_month')) <= int(form.data.get('dateStart_month')) and int(form.data.get('dateFinish_day')) < int(form.data.get('dateStart_day'))):
                    # вывод сообщения, что дата завершения не корректная 
                    print('Сообщение об ошибке неправильной формы даты. Дата завершения должна быть позже чем сегодня', form.data.get('dateStart_day'))
                    print('Данные', form.data)
                    form.add_error(None, 'Дата завершения не может быть раньше даты начала')
                    context = {
                    'form': form,
                    'count_todos' : count_todos,
                    'count_completed_todo' : count_completed_todo,
                    'uncompleted' : uncompleted,
                    }
                    return render(request, 'todos/update_task.html', context)
                else:
                    # форма редактирования содержит корректную информацию
                    form.save() # Сохранение формы
                    print("Данные сохранены")
                    return redirect('/') # Переход к корню сайта - Главной странице
            except Exception as e:
                print("Ошибка")
                logging.error(traceback.format_exc())
    else:
        # пользователь открыл форму для редактирования и еще не отправил данные
        form = UpdateTaskForm(instance=task)
 
    # контекст - переменные для отображания в html шаблоне
    context = {
        'form': form,
        'count_todos' : count_todos,
        'count_completed_todo' : count_completed_todo,
        'uncompleted' : uncompleted,
   
    }
    # отрисовка шаблона index.index и передача контекста переменных
    return render(request, 'todos/update_task.html', context)

# представление для удаления задачи по ИД
def delete(request, pk):
    # получаем задачу из БД по ИД
    task = Task.objects.get(id=pk)
    name_task = task.content
    # если пользователь подтвердил удаление
    if request.method == 'POST':
        # удаляем задачу из БД
        task.delete()
        # Возвращаем пользователя на главную страницу
        return redirect('/')
    # получаем весь список задач для вывода статистики
    todos = Task.objects.all() 
    count_todos = todos.count() # определяем кол-во всех задач
    # получаем выборку задач завершенных с помощью фильтра
    completed_todo = Task.objects.filter(complete=True) 
    count_completed_todo = completed_todo.count() # кол-во завершенных задач
    uncompleted = count_todos - count_completed_todo # вычисляем кол-во незавершенных задач
    # контекст - переменные для отображания в html шаблоне
    context = {
        'count_todos' : count_todos,
        'count_completed_todo' : count_completed_todo,
        'uncompleted' : uncompleted,
        'name_task' : name_task,
    }
    # если пользователь не отправил форму, то отрисовываем подтверждение об удалении задачи.
    return render(request, 'todos/delete_task.html', context)
