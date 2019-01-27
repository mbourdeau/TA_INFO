from django.urls import path
from . import views


urlpatterns = [
    # ex: /animalerie/
    path('', views.index, name='index'),
    # ex: /animalerie/action/
    path('action/', views.action, name='action')
]