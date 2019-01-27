from .models import Animal, Equipement


def nourrir(id_animal):
    if Equipement.verifie_disponibilite('mangeoire') == 'occupé':
        occupant = Animal.cherche_occupant('mangeoire')
        return 'Impossible, la mangeoire est actuellement occupée par ' + str(occupant)
    if Animal.lit_etat(id_animal) != 'affamé':
        return 'Désolé, ' + id_animal + ' n\'a pas faim !'
    else:
        Animal.change_lieu(id_animal, 'mangeoire')
        Animal.change_etat(id_animal, 'repus')


def divertir(id_animal):
    if Equipement.verifie_disponibilite('roue') == 'occupé':
        occupant = Animal.cherche_occupant('roue')
        return 'Impossible, la roue est actuellement occupée par ' + str(occupant)
    if Animal.lit_etat(id_animal) != 'repus':
        return 'Désolé, ' + id_animal + ' n\'est pas en état de faire du sport !'
    else:
        Animal.change_lieu(id_animal, 'roue')
        Animal.change_etat(id_animal, 'fatigué')


def coucher(id_animal):
    if Equipement.verifie_disponibilite('nid') == 'occupé':
        occupant = Animal.cherche_occupant('nid')
        return 'Impossible, le nid est actuellement occupée par ' + str(occupant)
    if Animal.lit_etat(id_animal) != 'fatigué':
        return 'Désolé, ' + id_animal + ' n\'est pas fatigué !'
    else:
        Animal.change_lieu(id_animal, 'nid')
        Animal.change_etat(id_animal, 'endormi')


def reveiller(id_animal):
    if Animal.lit_etat(id_animal) != 'endormi':
        return 'Désolé, ' + id_animal + ' ne dort pas !'
    else:
        Animal.change_lieu(id_animal, 'litière')
        Animal.change_etat(id_animal, 'affamé')
