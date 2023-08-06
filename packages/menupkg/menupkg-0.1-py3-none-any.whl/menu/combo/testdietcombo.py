import unittest
from menu.combo import dietcombo

class TestDietCombo(unittest.TestCase): # test class
    @classmethod
    def setUpClass(cls):
        #cls.set_data()
        print("setUpClass is running for testing regularcombo")
    #@classmethod
    #def set_data(cls):
        #cls.p1 = dietcombo.Dietcombo()
    @classmethod
    def tearDownClass(cls):
        print('tearDownClass is running for testing regularcombo')
    def setUp(self):
        self.p1 = dietcombo.Dietcombo(burger = ["big_mac"], snack = ["fries"], drink = ["diet","coca"])
        self.p1.burger_custom('lettuce')
        self.p2 = dietcombo.Dietcombo(burger = ["big_mac"], snack = ['chicken finger'], drink = ["coca"])
        self.p3 = dietcombo.Dietcombo(burger = ['quarter pound'], snack = ["fries"], drink = ["coca"])
        self.p4 = dietcombo.Dietcombo(burger = ["big_mac"], snack = ["fries"], drink = ["diet", "mtn dew"])
        self.p5 = dietcombo.Dietcombo(burger = "big_mac", snack = ["fries"], drink = ["diet", "mtn dew"])
        print('test method start')
    def tearDown(self):
        print('test method down')
    def test_calories_check(self):
        self.p2.snack_custom('fries')
        self.p2.snack_custom('fries')
        self.p4.burger_custom('double meat')
        self.p4.burger_custom('lettuce')
        self.assertEqual(self.p1.calories_check(), 'total calories OK')
        self.assertEqual(self.p2.calories_check(), 'warning: calories higher than standard!!!')
        self.assertEqual(self.p3.calories_check(), 'total calories OK')
        self.assertEqual(self.p4.calories_check(), 'warning: calories higher than standard!!!')
    def test_drink_check(self):
        self.assertEqual(self.p1.drink_check(), None)
        self.assertEqual(self.p2.drink_check(), 'warning: drink is not diet!')
        self.assertEqual(self.p3.drink_check(), 'warning: drink is not diet!')
        self.assertEqual(self.p4.drink_check(), None)
    def test_burger_cal_control(self):
        self.p1.burger_custom('double cheese')
        self.p3.burger_custom('tomato')
        self.assertEqual(self.p1.burger_cal_control(), 'Only regurlar burger provided in diet combo')
        self.assertEqual(self.p2.burger_cal_control(), None)
        self.assertEqual(self.p3.burger_cal_control(), 'Only regurlar burger provided in diet combo')
        self.assertEqual(self.p4.burger_cal_control(), None)
        self.assertEqual(self.p5.burger_cal_control(), 'enter burger type wrong, but OK in diet combo(no custom allowed)')
#unittest.main(argv =[''], verbosity=2, exit=False)
