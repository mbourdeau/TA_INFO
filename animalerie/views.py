from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
# Create your views here.
from .models import Animal
from .Controleur import nourrir, divertir, coucher, reveiller


def index(request):
    animal_list = Animal.objects.all()
    action_list = ['nourrir', 'divertir', 'coucher', 'réveiller']
    context = {'animal_list': animal_list, 'action_list': action_list}
    return render(request, 'animalerie/index.html', context)


def action(request):

    try:
        selected_animal = Animal.objects.get(pk=request.POST['id_animal'])
        selected_action = request.POST['actions']
    except (KeyError, Animal.DoesNotExist):
        return render(request, 'animalerie/action.html', {'error_message': "You didn't select a choice."})
    else:
        aux = ''
        if selected_action == 'nourrir':
            aux = nourrir(selected_animal.NAME)
        elif selected_action == 'divertir':
            aux = divertir(selected_animal.NAME)
        elif selected_action == 'coucher':
            aux = coucher(selected_animal.NAME)
        elif selected_action == 'réveiller':
            aux = reveiller(selected_animal.NAME)
        if aux == '' or aux is None:
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'animalerie/action.html', {'aux': aux})