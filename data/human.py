
class Human():

    EDAD = 0
    NAME = ''
    NATIONALITY = ''

    def __init__(self):
        self.comer()
        self.dormir()

    def comer(self):
        print('Comiendo ...\n')

    def dormir(self):
        print('Durmiendo ...\n')



class Employee(Human):

    def __init__(self):
        self.comer()


Employee()