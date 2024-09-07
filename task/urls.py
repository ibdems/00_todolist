from django.urls import path
from .views import *

urlpatterns = [
   path('', signin, name='signin'),
   path('logout/', signout, name='logout'),
   path('resistration/', registration, name='registration'),
   path('index/', index , name='index'),
   path('addCategory/', addCategory, name='addCategory'),
   path('addTask/', addTask, name='addTask'),
   path('<int:pk>/taskCategorie/', taskCategorie, name='task_categorie'),
   path('<int:id>/achevetask/', task_acheve, name='acheve_task')
]
