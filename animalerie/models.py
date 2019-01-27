from django.db import models
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.


class Animal(models.Model):
    NAME = models.CharField('Animal', max_length=50, primary_key=True)
    RACE_Choice = [('tamia', 'tamia'), ('hamster', 'hamster'), ('ili pika', 'ili pika'), ('opossum', 'opossum')]
    RACE = models.CharField(max_length=50, choices=RACE_Choice)
    TYPE_Choice = [('rongeur', 'rongeur'), ('marsupial', 'marsupial')]
    TYPE = models.CharField(max_length=50, choices=TYPE_Choice)
    ETAT_Choice = [('endormi', 'endormi'), ('affamé', 'affamé'), ('repus', 'repus'), ('fatigué', 'fatigué')]
    ETAT = models.CharField('ÉTAT', max_length=50, choices=ETAT_Choice)
    LIEU_Choice = [('litière', 'litière'), ('mangeoire', 'mangeoire'), ('nid', 'nid'), ('roue', 'roue')]
    LIEU = models.CharField(max_length=50, choices=LIEU_Choice)

    def __str__(self):
        return self.NAME

    @staticmethod
    def lit_etat(animal_id):
        try:
            animal = Animal.objects.get(pk=animal_id)
            return animal.ETAT
        except ObjectDoesNotExist:
            return None


    @staticmethod
    def lit_lieu(animal_id):
        try:
            animal = Animal.objects.get(pk=animal_id)
            return animal.LIEU
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def cherche_occupant(lieu):
        animals = Animal.objects.filter(LIEU=lieu)
        occupant = []
        for animal in animals:
            occupant.append(animal.NAME)
        if occupant == []:
            return None
        else:
            return occupant


    @staticmethod
    def change_etat(id_animal, etat):
        if (etat, etat) not in Animal.ETAT_Choice:
            return False
        try:
            animal = Animal.objects.get(pk=id_animal)
            animal.ETAT = etat
            animal.save()
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def change_lieu(id_animal, lieu):
        if (lieu, lieu) not in Animal.LIEU_Choice:
            return False
        if Equipement.verifie_disponibilite(lieu) == 'occupé':
            return False  # Désolé, le lieu XXX est déjà occupé.
        try:
            animal = Animal.objects.get(pk=id_animal)
            exlieu = Equipement.objects.get(pk=animal.LIEU)
            nvlieu = Equipement.objects.get(pk=lieu)
            exlieu.DISPO = 'libre'
            exlieu.save()
            if nvlieu.equipement != 'litière':
                nvlieu.DISPO = 'occupé'
                nvlieu.save()
            animal.LIEU = lieu
            animal.save()
            return True
        except ObjectDoesNotExist:
            return False


class Equipement(models.Model):
    equipement = models.CharField('Équipement', max_length=50, primary_key=True)
    DISPO_Choice = [('libre', 'libre'), ('occupé', 'occupé')]
    DISPO = models.CharField('	DISPONIBILITÉ', max_length=50, choices=DISPO_Choice)

    def __str__(self):
        return self.equipement

    @staticmethod
    def verifie_disponibilite(équipement_id):
        try:
            lieu = Equipement.objects.get(pk=équipement_id)
            return lieu.DISPO
        except ObjectDoesNotExist:
            return None

