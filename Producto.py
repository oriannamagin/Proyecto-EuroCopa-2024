class Producto():
    def __init__(self, name, quantity, price, stock, aditional):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.stock = stock
        self.aditional = aditional
        self.type = ""
        if aditional == "alcoholic" or aditional == "non-alcoholic":
            self.type = "Bebida"
        else:
            self.type  = "Comida"
        
    
    def show(self):
        print(self.type, self.price, self.name, self.quantity, self.stock)
    
    