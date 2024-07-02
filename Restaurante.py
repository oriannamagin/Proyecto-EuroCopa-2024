class Restaurante():
    def __init__(self, name, products):
        self.name =  name
        self.products = products 

    def show(self):
        print(self.name, self.products)