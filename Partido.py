class Partido():
    def __init__(self, local_team, visitor_team, date_time, stadium, id):
        self.local_team =  local_team
        self.visitor_team = visitor_team
        self.date_time = date_time
        self.stadium = stadium
        self.id = id
    
    def show(self):
        print(self.id, self.local_team.name, self.visitor_team.name, self.date_time, self.stadium.name)
    
    def show_corto(self):
        print(self.local_team.name, self.visitor_team.name, self.date_time, self.stadium.name)