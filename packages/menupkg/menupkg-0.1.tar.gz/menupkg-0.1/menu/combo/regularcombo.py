class Regularcombo():
    """docstring for ."""
    def __init__(self, burger = ["big_mac"], snack = ["fries"], drink = ["coca"]):
        try:
            assert type(burger) == list
        except AssertionError:
            print('Please enter initial burger as list then custom')
        else:
            self.burger = burger
        try:
            assert type(snack) == list
        except AssertionError:
            print('Please enter initial snack as list then custom')
        else:
            self.snack = snack
        try:
            assert type(drink) == list
        except AssertionError:
            print('Please enter initial drink as list then custom')
        else:
            self.drink = drink
        self.total = 0
    def burger_custom(self, extra):
        self.burger.append(extra)
    def snack_custom(self, extra):
        self.snack.append(extra)
    def drink_custom(self, extra):
        try:
            assert type(extra) == str
        except:
            return "Your custom value is not valid"
        try:
            if len(self.drink) > 3:
                raise DrinkcustomError()
        except DrinkcustomError:
            return "Your drink is too complex, please re-custom"
        else:
            self.drink.append(extra)
    def display(self):
        #print("burger:{},snack:{},drink:{}".format(self.burger, self.snack, self.drink))
        return '{} {} {}'.format(self.burger, self.snack, self.drink)
    def total_price(self):
        self.total = (len(self.burger)*4.99 + len(self.snack)*2.99 + 1.99)*1.15
        #print("total price is:{} CAD(Tax included)".format(self.total))
        return round(self.total,2)

class DrinkcustomError(Exception):
    pass
        
