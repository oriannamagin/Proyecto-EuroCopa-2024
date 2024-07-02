class Cliente():
    def __init__(self, name, id, age, ticket):
        self.name = name
        self.id = id
        self.age = age
        self.balance =  0
        self.ticket = ticket

    def show(self):
        print(self.id, self.age, self.name, self.ticket, self.balance)