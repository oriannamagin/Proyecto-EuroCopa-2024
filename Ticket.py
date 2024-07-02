class Ticket():
    def __init__(self,id,codigo_ticket,tipo_ticket, id_partido, asiento, asistencia):
        self.id = id
        self.codigo_ticket = codigo_ticket
        self.tipo_ticket =tipo_ticket
        self.id_partido = id_partido
        self.asiento = asiento
        self.asistencia = asistencia

    def show(self):
        print(self.codigo_ticket, self.tipo_ticket, self.id_partido, self.asiento, self.asistencia)
    