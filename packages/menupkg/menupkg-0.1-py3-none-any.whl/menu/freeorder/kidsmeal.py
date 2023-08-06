from menu.freeorder.regularorder import regularorder
from tabulate import tabulate

class kidsmeal(regularorder):
    def __init__(self, order=[], gift='Book'):
        regularorder.__init__(self,order = [])
        self.gift = gift
         
    def setGift(self,gift):
          self.gift = gift
        
    def menu(self):
          return (tabulate([['22. Cheeseburger', '26. Milk', '30. Apple Slice'], 
                           ['23. Hamburger', '27. Orange Juice','31. Chicken Nuggest'],
                           ['24. Chrispy Chicken Wrap', '28. Pineapple Smoothie','32. Mini Fry'],
                           ['25. Grilled Chicken Wrap', '29. Every Flavor Yoghurt','33. Carrot Muffin']], 
                           headers=['Burger & Wrap', 'Beverage','Snack']), "\n")
                 
    def review_order(self):
        if len(self.order) == 0:
            self.gift = 'None'
            x = "Please choose [Book] or [Toy] for this kids meal and no more than 4 items for the order!"
            return x
        elif len(self.order) > 4:
            self.gift = 'None'
            x = "Please review your order and make sure no more than 4 items selected for this kids meal, thank you!"
            return x
            self.order.clear()
        else:
            return (regularorder.review_order(self) + ' Gift: ' + str(self.gift))