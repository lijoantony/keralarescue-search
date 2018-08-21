from unittest import TestCase
from feeder.common.data import get_dist_name, get_location_concact


class Test_Data(TestCase):

    def test_get_dist_name(self):
        self.assertEqual(get_dist_name('ekm'), 'Ernakulam')
        self.assertEqual(get_dist_name(None), None)
        self.assertEqual(get_dist_name(''), None)
        self.assertEqual(get_dist_name('   '), None)
        self.assertEqual(get_dist_name('ekl'), None)
        self.assertEqual(get_dist_name('          ERNAKULAM'), 'Ernakulam')
        self.assertEqual(get_dist_name('alappuzha'), 'Alappuzha')

    def test_get_location_concact(self):
        loc = ("Apporu,Madrassa Palli,Mannancheery", "Apporu,Madrassa Palli,North aryad P.O,Mannancheery", None)
        self.assertEqual("Apporu,Madrassa Palli,Mannancheery, North aryad P.O,Mannancheery", get_location_concact(loc))