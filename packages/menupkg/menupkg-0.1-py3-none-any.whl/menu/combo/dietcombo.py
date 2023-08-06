from menu.combo.regularcombo import Regularcombo

class Dietcombo(Regularcombo):

    def __init__(self, burger = ["cheeseburger"], snack = ["fries"], drink = ["diet","coca"]):
        Regularcombo.__init__(self, burger, snack, drink)
    def calories_check(self):
        if self.drink[0] == "diet":
            total = (len(self.burger))*200 + (len(self.snack))*100
        else:
            total = (len(self.burger))*200 + (len(self.snack))*100 + (len(self.drink))*50
        if total > 500:
            return "warning: calories higher than standard!!!"
        else:
            return "total calories OK"
    def drink_check(self):
        if self.drink[0]!= "diet":
            return "warning: drink is not diet!"

    def burger_cal_control(self):
        try:
            assert type(self.burger) != str
        except:
            return "enter burger type wrong, but OK in diet combo(no custom allowed)"
        try:
            if len(self.burger) > 1:
                raise BurgercalError()
        except BurgercalError:
            self.burger = self.burger[0:1]
            return "Only regurlar burger provided in diet combo"

class BurgercalError(Exception):
    pass