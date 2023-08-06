import unittest
from menu.combo import regularcombo

class TestRegCombo(unittest.TestCase): # test class
    @classmethod
    def setUpClass(cls):
        #cls.set_data()
        print("setUpClass is running for testing regularcombo")
    #@classmethod
    #def set_data(cls):
        #cls.p1 = regularcombo.Regularcombo()
    @classmethod
    def tearDownClass(cls):
        print('tearDownClass is running for testing regularcombo')
    def setUp(self):
        self.p1 = regularcombo.Regularcombo(burger = ["big_mac"], snack = ["fries"], drink = ["coca"])
        self.p2 = regularcombo.Regularcombo(burger = ["big_mac"], snack = ['chicken finger'], drink = ["coca"])
        self.p3 = regularcombo.Regularcombo(burger = ['quarter pound'], snack = ["fries"], drink = ["coca"])
        self.p4 = regularcombo.Regularcombo(burger = ["big_mac"], snack = ["fries"], drink = ['mtn dew'])
        self.p5 = regularcombo.Regularcombo(burger = "big_mac", snack = "fries", drink = 'mtn dew')
        print('test method start')
    def tearDown(self):
        print('test method down')
    def test_burger_custom(self):
        self.p1.burger_custom('lettuce')
        self.p2.burger_custom('thousand island')
        self.p3.burger_custom('tomato')
        self.p4.burger_custom('no pickles')
        self.assertEqual(self.p1.burger, ['big_mac', 'lettuce'])
        self.assertEqual(self.p2.burger, ['big_mac', 'thousand island'])
        self.assertEqual(self.p3.burger, ['quarter pound', 'tomato'])
        self.assertEqual(self.p4.burger, ['big_mac', 'no pickles'])
    def test_snack_custom(self):
        self.p1.snack_custom('chicken finger')
        self.p2.snack_custom('fries')
        self.p3.snack_custom('nuggets')
        self.p4.snack_custom('chicken wing')
        self.assertEqual(self.p1.snack, ['fries', 'chicken finger'])
        self.assertEqual(self.p2.snack, ['chicken finger', 'fries'])
        self.assertEqual(self.p3.snack, ['fries', 'nuggets'])
        self.assertEqual(self.p4.snack, ['fries', 'chicken wing'])
    def test_drink_custom(self):
        self.p1.drink_custom('no ice')
        self.p2.drink_custom('double ice')
        self.p4.drink_custom('double ice')
        self.p4.drink_custom('double cream')
        self.p4.drink_custom('double cream')
        self.assertEqual(self.p1.drink, ['coca', 'no ice'])
        self.assertEqual(self.p2.drink, ['coca', 'double ice'])
        self.assertEqual(self.p3.drink_custom(['sprite', 'mtn dew']), 'Your custom value is not valid')
        self.assertEqual(self.p4.drink_custom('double cream'), 'Your drink is too complex, please re-custom')
    def test_display(self):
        self.p1.burger_custom('lettuce')
        self.p2.snack_custom('fries')
        self.p4.drink_custom('double ice')
        self.assertEqual(self.p1.display(), "['big_mac', 'lettuce'] ['fries'] ['coca']")
        self.assertEqual(self.p2.display(), "['big_mac'] ['chicken finger', 'fries'] ['coca']")
        self.assertEqual(self.p3.display(), "['quarter pound'] ['fries'] ['coca']")
        self.assertEqual(self.p4.display(), "['big_mac'] ['fries'] ['mtn dew', 'double ice']")
    def test_total_price(self):
        self.p1.burger_custom('lettuce')
        self.p2.snack_custom('fries')
        self.p4.drink_custom('double ice')
        self.assertEqual(self.p1.total_price(), 17.2)
        self.assertEqual(self.p2.total_price(), 14.9)
        self.assertEqual(self.p3.total_price(), 11.47)
        self.assertEqual(self.p4.total_price(), 11.47)
#unittest.main(argv =[''], verbosity=2, exit=False)