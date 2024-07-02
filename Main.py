import requests
import json
import uuid
from Equipo import Equipo
from Estadio import Estadio
from Partido  import Partido
from Restaurante import Restaurante
from Producto import Producto
from Ticket import Ticket
from Cliente import Cliente

def api(equipos, partidos, estadios):

    ###Equipos
    #llamamos a cada diccionario para importar la informacion de cada uno
    url_equipo = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/teams.json"
    #trae la informacion del API y la guarda como texto en una variable
    response = requests.get(url_equipo)
    #te transforma  ese texto a  un json
    response = response.json()
    
    for equipo in response:
        new_equipo = Equipo(equipo["id"], equipo["code"], equipo["name"], equipo["group"])
        equipos.append(new_equipo)


    ###Estadios
    url_estadio = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json"
    response = requests.get(url_estadio)
    response = response.json()
    
    for estadio in response:
        
        restaurantes = []
        for restaurante in estadio["restaurants"]:
            products=[]
            for product in restaurante["products"]:
                new_product = Producto(product["name"], product["quantity"], product["price"], product["stock"], product["adicional"])
                products.append(new_product)

            restaurant =Restaurante(restaurante["name"], products)
            restaurantes.append(restaurant)


        new_estadio = Estadio(estadio["name"],estadio["city"],estadio["capacity"],estadio["id"], restaurantes)
        estadios.append(new_estadio)


    ###Partidos
    url_partido = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/matches.json"
    response = requests.get(url_partido)
    response = response.json()

    for partido in response:
        #Recorrer informacion por diccionario para obtener el objeto que coincide con el id dado
        for equipo in  equipos:
            id_dicc = partido["home"]["id"]
            if equipo.id == id_dicc:
                local_team = equipo

        for equipo in  equipos:
            id_dicc = partido["away"]["id"]
            if equipo.id == id_dicc:
                visitor_team = equipo
    
        #Ubicar el id de cada estadio para poder ubicarlo en el diccionario y arrojar la info correspondiente
        for estadio in estadios:
            id = partido["stadium_id"]
            if estadio.id == id:
                stadium = estadio
                
        #Objeto tipo partido con la información correspondiente al diccionario
        new_partido = Partido(local_team, visitor_team, partido["date"], stadium, partido["id"])
        partidos.append(new_partido)
       
def menu(options):
    for i, option in enumerate(options):
        print(f"{i+1}. {option}")

    option = input("Indique la opcion que desea ver: ")
    while not option.isnumeric() or not int(option) in range(1, len(options)+1):
        option = input("La  opcion  ingresada no es correcta. Intente de nuevo")
    
    option = int(option)-1
    return option

def partidos_estadios(partidos):
    print("Bienvenido, escoja  la funcion que desea: ")
    options = ["Partidos de un pais: ","Partidos por estadio: ","Partidos por fecha: ", "Salir"]
    while True:
        option = menu(options)
        if option == 0:
            print("Partidos de un pais")
            
            name = input("Ingrese el nombre del pais que desea buscar: ")

            for partido in partidos:
                if name == partido.local_team.name.capitalize() or name == partido.visitor_team.name.capitalize():
                    partido.show()

        elif option == 1:
            print("Partidos por estadio")

            games = input("Ingrese el estadio que desea visitar: ").capitalize()

            for partido in partidos:
                if games == partido.stadium.name.capitalize():
                    partido.show()

        elif option == 2:
            print("Partidos por fecha")
            #arreglar todos los buscadorescon.capitalize()
            time = input("Ingrese la fecha del partido que desea (dd-mm-yy): ").capitalize()

            for partido  in partidos:
                if time == partido.date_time.name.capitalize():
                    partido.show()

        elif option == 3:
            print("Hasta Luego")
            break 

def venta_entradas(partidos, tickets, clientes):
    print("Bienvenido! para comprar sus  entradas ingrese los siguientes datos: ")
    name = input("Nombre y Apellido: ")
    id = input("Cedula: ")
    age = input("Edad: ")

    print("Aqui te mostramos los partidos: ")
    for posicion, partido in enumerate(partidos, start=1):
        print(posicion, end=" ")
        partido.show_corto()
    game = input("Indique el numero del partido que desea ver: ")
    while not game.isnumeric():
        game = input("Indique el numero del partido que desea ver: ")
    partido = partidos[int(game)-1]

    print("ASIENTOS")
    print("1. Entrada General")
    print("2. Entrada VIP")
    seat= input("Indique el numero del tipo de entrada que desea comprar: ")
    while seat != "1" and seat != "2":
        seat  = input("Indique el numero del tipo de entrada que desea comprar: ")

    precio = 0
    if seat == "1":
        precio = 35
        seat = "General"
        cantidad_asientos = partido.stadium.capacity[0]
    elif seat == "2":
        precio = 75
        seat = "VIP"
        cantidad_asientos = partido.stadium.capacity[1]
    
    cantidad_fila = cantidad_asientos//10

    letras = "ABCDEFGHIJ"
    for fila in range(1, cantidad_fila):
        lista_fila = []
        for letra in letras:
            asiento = letra+str(fila)
            lista_fila.append(asiento)
        
        print(lista_fila)
    
    asiento_letras = input("Ingrese la letra del asiento que desea: ").upper()
    while not asiento_letras in letras:
        asiento_letras = input("Ingrese la letra del asiento que desea: ").upper()
    asiento_numero= input("Ingrese el numero del asiento que desea")
    while not asiento_numero.isnumeric() or not int(asiento_numero) in range(1, cantidad_fila+1):
        asiento_numero= input("Ingrese el numero del asiento que desea")

    descuento = 0
    validar = es_vampiro(int(id))
    if validar == True:
        descuento = precio/2
    
    iva = precio*0.16

    asiento = asiento_letras+asiento_numero
    id_unico = uuid.uuid4()
    id_unico_str = ("{:032x}".format(id_unico.int))[1:33].lower()
    codigo_asiento = f"{id_unico_str[:8]}-{id_unico_str[8:12]}-{id_unico_str[12:16]}-{id_unico_str[16:20]}-{id_unico_str[20:]}"

    print("*** FACTURA ***")
    print(f'''Cliente:{name}
          Asiento: {asiento}
          Codigo del asiento: {codigo_asiento}
          Subtotal:{precio}
          Descuento:{descuento}
          IVA:{iva}
          Total:{precio - descuento + iva}
          ''')
    
    print("Desea proceder con su compra?")
    print("1. SI")
    print("2. NO")
    compra = input("Indique la opcion seleccionada: ")
    while compra != "1" and compra != "2":
        compra = input("Indique la opcion seleccionada: ")

    if compra == "1":
        #para generar el ticket vendido
        print("SU COMPRA SE HA REALIZADO CON EXITO!")
        nuevo_ticket = Ticket(id,codigo_asiento, seat, partido, asiento, False)
        tickets.append(nuevo_ticket)
        nuevo_cliente = Cliente(name, age, id, nuevo_ticket)
        nuevo_cliente.balance += precio - descuento + iva
        clientes.append(nuevo_cliente)
    elif compra == "2":
        print("HASTA LUEGO")

def es_vampiro(numero):
    digitos = list(str(numero))
    num_digitos = len(digitos)

    # Comprobación de los factores
    for i in range(1, int(numero**0.5)+1):
        if numero % i == 0:
            factor1 = str(i)
            factor2 = str(numero // i)
            factores = factor1 + factor2

            # Comprobación de la permutación
            if sorted(digitos) == sorted(factores) and len(factor1) == len(factor2):
                return True

    return False

def asistencia(tickets):
    codigo = input("Ingrese el codigo de su ticket: ")
    contador = 0
    
    for ticket in tickets:
        if codigo.lower() == ticket.codigo_ticket.lower() and ticket.asistencia != True:
            contador = 1
            print("ASISTENCIA VALIDA!")
            ticket.asistencia = True
    if contador == 0:
        print("ASISTENCIA INVALIDA!")

def restaurantes(productos, tickets, partidos, clientes):
    #Pedirle al usuario el numero de cedula para comprobar si este pertenece al grupo de entradas VIP
    print("BIENVENIDO! PARA COMPRAR EN EL RESTAURANTE DEBE SER CLIENTE VIP")
    id = input("Ingrese su numero de  cedula: ")
    contador = 0

    for ticket in tickets:
        if id.lower() == ticket.id.lower() and ticket.tipo_ticket == "VIP":
            contador = 1
            print("Usted es usuario VIP, a continuacion le mostramos la lista de restaurantes:")
            compra(ticket, partidos, id, clientes)

    if contador == 0:
        print("Su cedula no coincide con los usuarios VIP")

def busqueda_productos(productos):
    print('''Seleccione el tipo de busqueda que desea realizar: 
          1. Por nombre
          2. Por tipo
          3. Por rango de precio''')
    option = input("Indique el numero de la opcion de su preferencia: ")

    if option == 1:
        name = input("Ingrese el nombre del producto que desea ver: ")
        for producto in productos:
            if name in producto.name:
                producto.show()
    elif option == 2:
        type = input("Ingrese el typo del producto que desea ver (alimento, bebida): ")
        for producto in productos:
            if type in producto.type:
                producto.show()
    elif option == 3:
        lowest_price = input("Desde: ")
        highest_price = input("Hasta: ")
        for producto in productos:
            if lowest_price <= producto.price and highest_price >= producto.price:
                producto.show()
    else:
        print("La opcion ingresada no es valida!")
    
def compra(ticket, partidos, id, clientes):

    age = 0
    for cliente in clientes:
        if cliente.id == id:
            age = cliente.age

    restaurantes = ""
    partido_id = ticket.id_partido
    for partido in partidos:
        if partido_id.id == partido.id:
            restaurantes = partido.stadium.restaurantes

    for indice,restaurante in enumerate(restaurantes, start=1):
        
        print(indice, restaurante.name)
    option = input("Ingrese el numero del restaurante de  su preferencia: ")
    productos = restaurantes[int(option)-1].products

    print("Le mostramos los productos disponibles!")
    for indice, producto in enumerate(productos, start=1):
        print(indice,producto.name)
    option_2 = input("Ingrese la opcion del producto que desea: ")
    #validar quje el numero este en el rango de cantidad de productos
    while age < 18 and productos[len(productos)-1].aditional == "alcoholic":
        print("Un menor de edad no puede comprar alcohol")
        option_2 = input("Ingrese la opcion del producto que desea: ")
    
    producto = productos[int(option_2)-1]
    cantidad = input("Indique la cantidad del que desea del producto: ")
    while not cantidad.isnumeric() or int(cantidad) < 0:
        cantidad = input("Indique la cantidad que desea del producto: ")

    

    cantidad_int = int(cantidad)
    producto.quantity - cantidad_int

    info_producto = producto.name
    precio_producto = float(producto.price)
    descuento = 0
    validar = es_perfecto(int(id))
    if validar == True:
        descuento = precio_producto*0.15
    iva = precio_producto*0.16

    print("*** FACTURA ***")
    print(f'''
          - Cedula:{id}
          - Producto: {info_producto}
          - Subtotal:{precio_producto}
          - Descuento:{descuento}
          - IVA:{iva}
          - Total:{precio_producto - descuento + iva}
          ''')
    print("Desea proceder con su compra?")
    print("1. SI")
    print("2. NO")
    compra = input("Indique la opcion seleccionada: ")
    while compra != "1" and compra != "2":
        compra = input("Indique la opcion seleccionada: ")
    
    if compra == "1":
        print("SU COMPRA SE HA REALIZADO CON EXITO!")
        
    elif compra == "2":
        print("HASTA LUEGO")
    
def es_perfecto(numero):
    suma_divisores = 0
    for i in range(1, numero):
        if numero % i == 0:
            suma_divisores += i
    return suma_divisores == numero

def indicadores():
    print("Para ver los indicadores que desee escoja la opcion de su preferencia:")
    options = ["Gastos x Partidos VIP: ","Ranking mejor a peor ","Partido de mayor asistencia: ", "Partido mas vendido: ", "Top 3 productos Rest: ", "Top 3 clientes", "Graficos", "Salir"]
    while True:
        option = menu(options)
        if option == 0:
            print("Gastos x Partidos VIP")
        elif option == 1:
           print("Ranking mejor a peor")
        elif option == 2:
            print("Partido de mayor asistencia")
        elif option == 3:
            print("Partido mas vendido")
        elif option == 4:
             print("Top 3 productos Rest")
        elif option == 5:
            print("Top 3 clientes")
        elif option == 6:
             print("Graficos")
        elif option == 7:
            print("Hasta Luego")
            break

def main():
    equipos =[]
    partidos = []
    estadios = []
    tickets = []
    clientes = []
    productos = []

    api(equipos, partidos, estadios)

    print("Bienvenido")
    options = ["Partidos y Estadios","Venta de entradas","Asistencia a partidos", "Restaurantes", "Busqueda de productos", "Indicadores de gestion", "Salir"]
    while True:
        option = menu(options)
        if option == 0:
            partidos_estadios(partidos)
        elif option == 1:
            venta_entradas(partidos, tickets, clientes)
        elif option == 2:
            asistencia()
        elif option == 3:
            restaurantes(productos, tickets, partidos, clientes)
        elif option == 4:
            busqueda_productos(productos)
        elif option == 5:
            indicadores()
        elif option == 6:
            print("Hasta Luego")
            break

def write():
    archivo = open('archivo.txt','r')
    datos = archivo.read()
    archivo.close()
    print(datos)

    
main()



