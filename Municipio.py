from Localidad import Localidad


class Municipio:
#Aqui tenemos el municipio donde se coloca el nombre y las distintas localidades que tiene
    def __init__(self, el_nombre):
        self.nombre = el_nombre
        self.localidades = []
    #En este caso, las localidades van en una lista ya que son varias y se guardara alli toda esa informacion

    def __str__(self):
        return(f"Municipio:{self.nombre} y sus localidades {len(self.localidades)}")
    #Aqui se mostrara toda la informacion del municipio. Ademas las localidades van a ir uno por una


    def agregar_localidad(self, la_localidad):
        self.localidades.append(la_localidad)
    #Aqui se agregara la localidad en la lista a cada una de ellas


    def localidades_con_coordenadas(self):
        validas = []
        for loc in self.localidades:
            if loc.tiene_coordenadas():
                validas.append(loc)
        return validas
    #Aqui se permitira poner las coordenadas de las localidades que lo posean y sea visible
    

    def reporte_inicial(self):
        """esta funcion debe imprimir por el municipio la cantidad de localidades cargadas,
        las que tienen coordenadas geograficas, las que no y el porcentaje"""
        localidades_totales = len(self.localidades)
        localidades_coordenadas = len(self.localidades_con_coordenadas())
        localidades_sin_coordenadas = localidades_totales - localidades_coordenadas

        if localidades_totales > 0:
            porcentaje_localidades_coordenadas = round(((localidades_coordenadas / localidades_totales) * 100), 2)
        else:
            porcentaje_localidades_coordenadas = 0
        #para mostrarlo en pantalla
        print(f"Para el municipio {self.nombre}, se han cargado {localidades_totales} localidades.\n{localidades_coordenadas} tienen coordenadas y {localidades_sin_coordenadas} no tienen\nPorcentaje: {porcentaje_localidades_coordenadas}%")


    def seleccionar_localidad(self):
        """esta funcion debe mostrar la lista de localidades con su indice, de manera que el usuario ingrese el que quiera consultar"""
        localidades_validas = self.localidades_con_coordenadas()

        if len(localidades_validas) == 0:
            print("Este municipio no posee localidades que tengan coordenadas validas. Disculpe!")
        else:
            print("---------------------------------------------------------------------------------")
            print(f"                     Localidades de {self.nombre}")
            print("---------------------------------------------------------------------------------")
            for i, loc in enumerate(localidades_validas):
                print(f"{i+1}- {loc.nombre}")
            """debe buscar la opcion elegida por el usuario y retornar el municipio que quiere consultar"""
            seguir = True
            while seguir:
                opcion = (input("Ingresa la localidad que quieras consultar: "))
            #Comprueba si la opcion es numerica antes de entrar a los condicionales 
                if opcion.isdigit() == True:
                    opcion = int(opcion)
                    #Comprueba y devuelve el municipio elegido
                    if opcion > len(localidades_validas) or opcion <= 0:
                        print("Selecciona una localidad dentro del rango.")
                    else: 
                        seguir = False
                        return localidades_validas[opcion - 1]
                else:
                    print("No ingreses letras ni simbolos, por favor.")