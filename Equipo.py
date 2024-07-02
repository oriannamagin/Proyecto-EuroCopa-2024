
class Equipo():
    def __init__(self, id, code, name,  group):
        self.id = id
        self.code = code
        self.name = name
        self.group = group
    
    def show(self):
        print(self.id, self.code, self.name, self.group)

    