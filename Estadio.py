class Estadio():

    def __init__(self, name, city, capacity, id, restaurantes):
        self.name  = name
        self.city = city
        self.id = id
        self.capacity = capacity
        self.restaurantes = restaurantes

    def show(self):
        print(self.id, self.name, self.city, self.capacity, self.restaurantes)