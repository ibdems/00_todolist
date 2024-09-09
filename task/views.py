from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages
from task.forms import CategorieForm, RegistrationForm, SiginForm, TaskForm
from task.models import Categorie, Task
from django.utils import timezone

# Create your views here.
def signin (request):
    if request.method == 'POST':
        form = SiginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('index'))
            else:
                messages.error(request, "L'utilisateur saisi n'existe pas")
                return redirect(reverse('signin'))
        else:
            print(form.errors)
            return redirect(reverse('signin'))
    else:
        form = SiginForm()
    return render(request, 'signin.html', {'form': form})

def signout(request):
    logout(request)
    return redirect(reverse('signin'))

def registration (request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = User.objects.create_user(
                username=cleaned_data.get('username'),
                email=cleaned_data.get('email'),
                password=cleaned_data.get('password'),
                last_name=cleaned_data.get('last_name'),
                first_name=cleaned_data.get('first_name')
            )
            user.save()
            return redirect(reverse('signin'))
        else :
            print(form.errors)
            return redirect(reverse('registration'))
    else:
        form = RegistrationForm()
     
    return render(request, 'registration.html', {'form': form})

def trie(request, tasks):
    filter_date = request.GET.get('date')
    priority_task = request.GET.get('priority')
    status_task = request.GET.get('status')
    today = timezone.now().date()

    if filter_date:
        if filter_date == 'today':
            tasks = tasks.filter(start_date__lte=today, end_date__gte=today)
        elif filter_date == 'futur':
            tasks = tasks.filter(start_date__gt=today)
        elif filter_date == 'passe':
            tasks = tasks.filter(end_date__lt=today)
    
    if priority_task:
        tasks = tasks.filter(priority__iexact=priority_task.capitalize())

    if status_task:
        if status_task == 'termine':
            tasks = tasks.filter(status=True)
        elif status_task == 'nontermine':
            tasks = tasks.filter(status=False)

    return tasks

def taskCategorie(request, pk):
    categories = Categorie.objects.all()
    categorie = Categorie.objects.get(pk=pk)
    tasks = Task.objects.filter(categorie=categorie).order_by('-start_date')  

    tasks = trie(request, tasks)
    context = {
        'tasks': tasks,
        'categories': categories,
        'today': timezone.now().date(),
    }
    
    return render(request, 'index.html', context)   

@login_required(login_url='/signin/')
def index(request):
    categories = Categorie.objects.all()
    formCategory = CategorieForm()
    formTask = TaskForm()
    tasks = Task.objects.all()

    tasks = trie(request, tasks)
    context = {
        'categories': categories,
        'formCategory': formCategory,
        'formTask': formTask, 
        'tasks': tasks,
        'today': timezone.now().date
    }
        
    return render(request, 'index.html', context)


def addCategory(request):
    if request.method == 'POST':
        formCategory = CategorieForm(request.POST)
        if formCategory.is_valid():
            formCategory.save()
            messages.success(request, 'Categorie bien enregistrer')
            return redirect(reverse('index'))
        else :
            print(formCategory.errors)
            messages.error(request, 'Categorie non enregistrer')
            return redirect(reverse('index'))
    else :
        formCategory = CategorieForm()
        context = {'formCategory': formCategory}
        
    return render(request, 'addCategory.html', context) 

def addTask(request):
    if request.method == 'POST':
        formTask = TaskForm(request.POST)
        if formTask.is_valid():
            formTask.save()
            messages.success(request, 'Tâche bien enregistrer')
            return redirect(reverse('index'))
        else :
            print(formTask.errors)
            messages.error(request, 'Tâche non enregistrer')
            return redirect(reverse('index'))
    else :
        formTask = TaskForm()
        context = {'formTask': formTask}
        
    return render(request, 'addTask.html', context)


def task_acheve(request, id):
    task = Task.objects.get(id=id)
    task.status = True
    task.save()
    messages.success(request, 'Tâche terminé')
    return redirect(reverse('index'))