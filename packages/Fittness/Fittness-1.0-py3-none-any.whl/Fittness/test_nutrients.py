import unittest
import Fittness.calories_intake.nutrients as nu

class TestNutrients(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.s1 = nu.Nutrients('protein', 75)
        cls.s2 = nu.Nutrients('fat', 40)
        cls.s3 = nu.Nutrients('carbohydrate', 165)
        print('setUpClass')
        
    def setUp(self):
        self.n1 = nu.Protein('protein', 75, 4)
        self.n2 = nu.Fat('fat', 40, 9)
        self.n3 = nu.Carbohydrate('carbohydrate', 165, 4)
        
    def test_protCal(self):
        self.assertEqual(self.n1.protCal(), 300)
        
    def test_fatCal(self):
        self.assertEqual(self.n2.fatCal(), 360)
        
    def test_carbCal(self):
        self.assertEqual(self.n3.carbCal(), 660)
        
    def test_calCalories(self):
        self.assertEqual(nu.calCalories(75, 40, 165), 1320)
        self.assertEqual(nu.calCalories(0, 84, 120), 1236)
        self.assertEqual(nu.calCalories(82, 110, 0), 1318)
        self.assertEqual(nu.calCalories(57, 0, 189), 984)
        
    def test_bodyNeeds(self):
        self.assertEqual(nu.bodyNeeds(45, 160, 'f', 30, 75, 40, 165, 1.2), 'You need to intake more calories daily!')
        self.assertEqual(nu.bodyNeeds(55, 176, 'm', 67, 150, 120, 250, 1.375), 'You need to cut down your daily calorie intake or do more exercise!')
        self.assertEqual(nu.bodyNeeds(52, 170, 'f', 32, 120, 85, 199, 1.55), 'You are doing great to maintain your weight!')
        self.assertEqual(nu.bodyNeeds(85, 180, 'm', 45, 250, 120, 350, 1.9), 'You need to intake more calories daily!')
    
    def tearDown(self):
        self.n1 = None
        self.n2 = None
        self.n3 = None
        
    @classmethod
    def tearDownClass(cls):
        cls.s1 = None
        cls.s2 = None
        cls.s3 = None
        print('tearDownClass')

unittest.main(argv=[''], verbosity=2, exit=False)