from django.test import TestCase
from .models import Animal, Equipement
from .Controleur import nourrir
# Create your tests here.


class ModelTests(TestCase):

    def setUp(self):
        Animal.objects.create(NAME='Tic', RACE='tamia', TYPE='rongeur', ETAT=Animal.ETAT_Choice[1][1], LIEU='litière')
        Animal.objects.create(NAME='Tac', RACE='tamia', TYPE='rongeur', ETAT='affamé', LIEU='litière')
        Animal.objects.create(NAME='Patrick', RACE='hamster', TYPE='rongeur', ETAT='affamé', LIEU='litière')
        Animal.objects.create(NAME='Totoro', RACE='ili pika', TYPE='rongeur', ETAT='repus', LIEU='mangeoire')
        Animal.objects.create(NAME='Pocahontas', RACE='opossum', TYPE='marsupial', ETAT='endormi', LIEU='nid')

        Equipement.objects.create(equipement='litière', DISPO='libre')
        Equipement.objects.create(equipement='mangeoire', DISPO='occupé')
        Equipement.objects.create(equipement='roue', DISPO='libre')
        Equipement.objects.create(equipement='nid', DISPO='occupé')

    def test_lit_etat(self):
        assert Animal.lit_etat(animal_id='Tic') == Animal.ETAT_Choice[1][1]

    def test_lit_etat_nul(self):
        assert Animal.lit_etat('Bob') is None

    def test_lit_lieu(self):
        assert Animal.lit_lieu('Tac') == 'litière'

    def test_lit_lieu_nul(self):
        assert Animal.lit_lieu('Bob') is None

    def test_verifie_disponibilite(self):
        assert Equipement.verifie_disponibilite('litière') == 'libre'
        assert Equipement.verifie_disponibilite('nid') == 'occupé'

    def test_verifie_disponibilite_nul(self):
        assert Equipement.verifie_disponibilite('nintendo') is None

    def test_cherche_occupant(self):
        assert Animal.cherche_occupant('nid') == ['Pocahontas']
        assert 'Tac' in Animal.cherche_occupant('litière')
        assert 'Tac' not in Animal.cherche_occupant('mangeoire')

    def test_cherche_occupant_nul(self):
        assert Animal.cherche_occupant('casino') is None

    def test_change_etat(self):
        Animal.change_etat('Totoro', 'fatigué')
        assert Animal.lit_etat('Totoro') == 'fatigué'
        Animal.change_etat('Totoro', 'excité comme un pou')
        assert Animal.lit_etat('Totoro') == 'fatigué'
        Animal.change_etat('Bob', 'fatigué')
        assert Animal.lit_etat('Bob') is None

    def test_change_lieu(self):
        Animal.change_lieu('Totoro', 'roue')
        self.assertEqual(Animal.lit_lieu('Totoro'), 'roue')
        self.assertEqual( Equipement.verifie_disponibilite('mangeoire'), 'libre')
        self.assertEqual( Equipement.verifie_disponibilite('roue'), 'occupé')

    def test_change_lieu_occupe(self):
        Animal.change_lieu('Totoro', 'nid')
        self.assert_(Animal.lit_lieu('Totoro') == 'mangeoire')

    def test_change_lieu_nul_1(self):
        Animal.change_lieu('Totoro', 'casino')
        self.assert_(Animal.lit_lieu('Totoro') == 'mangeoire')

    def test_change_lieu_nul_2(self):
        Animal.change_lieu('Bob', 'litière')
        assert Animal.lit_lieu('Bob') is None

class ControleurTests(TestCase):

    def setUp(self):
        Animal.objects.create(NAME='Tic', RACE='tamia', TYPE='rongeur', ETAT='affamé', LIEU='litière')
        Animal.objects.create(NAME='Tac', RACE='tamia', TYPE='rongeur', ETAT='affamé', LIEU='litière')
        Animal.objects.create(NAME='Patrick', RACE='hamster', TYPE='rongeur', ETAT='affamé', LIEU='litière')
        Animal.objects.create(NAME='Totoro', RACE='ili pika', TYPE='rongeur', ETAT='repus', LIEU='mangeoire')
        Animal.objects.create(NAME='Pocahontas', RACE='opossum', TYPE='marsupial', ETAT='endormi', LIEU='nid')

        Equipement.objects.create(equipement='litière', DISPO='libre')
        Equipement.objects.create(equipement='mangeoire', DISPO='libre')
        Equipement.objects.create(equipement='roue', DISPO='libre')
        Equipement.objects.create(equipement='nid', DISPO='occupé')

    def test_nourrir(self):
        if Equipement.verifie_disponibilite('mangeoire') == 'libre' and Animal.lit_etat('Tic') == 'affamé':
            nourrir('Tic')
        assert Equipement.verifie_disponibilite('mangeoire') == 'occupé'
        self.assertEqual(Animal.lit_etat('Tic'), 'repus')
        assert Animal.lit_lieu('Tic') == 'mangeoire'
        nourrir('Tac')
        assert Animal.lit_etat('Tac') == 'affamé'
        assert Animal.lit_lieu('Tac') == 'litière'
        nourrir('Pocahontas')
        assert Animal.lit_etat('Pocahontas') == 'endormi'
        assert Animal.lit_lieu('Pocahontas') == 'nid'
        nourrir('Bob')
        assert Animal.lit_etat('Bob') is None
        assert Animal.lit_lieu('Bob') is None
        assert Equipement.verifie_disponibilite('mangeoire') == 'occupé'


