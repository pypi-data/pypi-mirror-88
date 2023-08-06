import unittest
from menu.freeorder.regularorder import regularorder

class orderError(Exception):
    pass

class test_regular(unittest.TestCase):  
    @classmethod
    def setUpClass(cls):
        print('Set Up Test for module: regularorder')
        
    def setUp(self): 
        self.r1 = regularorder()
        self.r1.burger(1)
        self.r1.burger(3)
        self.r2 = regularorder()
        self.r2.beverage(9)
        self.r2.beverage(10)
        self.r3 = regularorder()
        self.r3.snack(15)
        self.r3.snack(17)
        self.r4 = regularorder()
        self.r4.snack(15)
        self.r4.next_customer()
        print('Set Up Each Test')
        
    def test_burger(self):
        try:
            self.assertIsNotNone(self.r1.order)
            self.assertEqual(self.r1.price, (5.3+3.2))
            self.assertIn('Big Mac', self.r1.order)
            self.assertEqual(self.r1.order[1], 'Mighty Angus')
            self.r1.burger('mac')
            r1.burger(1)
        except NameError:               
            print("## Error! Order not defined!")

    def test_beverage(self):  
        try:
            self.assertIsNotNone(self.r2.order)
            self.assertEqual(self.r2.price, (1.2+1.1))
            self.assertIn('Ice Tea', self.r2.order)
            self.assertEqual(self.r2.order[0], 'Diet Coke')
            self.r1.beverage('Coke')
            r1.beverage(10)
        except NameError:               
            print("## Error! Order not defined!")
            
        
    def test_snack(self):    
        try:
            self.assertTrue(self.r3.order == ['Poutine', 'Fries'])
            self.assertEqual(self.r3.price, (3.2+2.1))
            self.assertNotIn('Coke', self.r3.order)
            self.assertNotEqual(self.r3.order[0], 'Diet Coke')
            self.r1.snack("McFlurry")
            r1.snack(20)
        except NameError:               
            print("## Error! Order not defined!")
          
    def test_menu(self):     
        try:
            self.assertIsNotNone(self.r1.menu())
            self.assertIsNotNone(self.r2.menu())
            self.assertIsNotNone(self.r3.menu())
            self.assertIsNotNone(self.r4.menu())
            self.assertIsNotNone(r4.menu())
        except NameError:               
            print("## Error! Order not defined!")
    
    def test_reviewOrder(self):             
        try:
            self.assertEqual(self.r1.review_order(), 'Your Orders: ' + ''.join(self.r1.order) + ' Price: 8.5 GST(5%): 0.43 PST(7%): 0.6 Total: 9.52')
            self.assertEqual(self.r2.review_order(), 'Your Orders: ' + ''.join(self.r2.order) + ' Price: 2.3 GST(5%): 0.11 PST(7%): 0.16 Total: 2.58')
            self.assertEqual(self.r3.review_order(), 'Your Orders: ' + ''.join(self.r3.order) + ' Price: 5.3 GST(5%): 0.27 PST(7%): 0.37 Total: 5.94')
            self.assertEqual(self.r4.review_order(), 'Your Orders: ' + ''.join(self.r4.order) + ' Price: 0 GST(5%): 0.0 PST(7%): 0.0 Total: 0.0')
            self.assertIsNotNone()
        except TypeError:               
            print("## Error! Please input the correct order number!")

    def test_next(self):    
        try:
            self.assertTrue(self.r4.order == [])
            self.assertEqual(self.r4.price, 0)
            self.assertNotIn('Coke', self.r4.order)
            self.assertTrue(len(self.r4.order) == 0)
            if len(self.r1.order) != 0:
                raise orderError
        except orderError:
            print("## Error! Make sure to clear out the orders before serving the next customer !")
        
    def tearDown(self):                                       
        print('Tear Down Each Test')

    @classmethod
    def tearDownClass(cls):
        print('Tear Down Test for module: regularorder')
                
        
unittest.main(argv=[''], verbosity=2, exit=False)  


