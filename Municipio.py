from Localidad import Localidad


class Municipio:
    """
    Clase que representa un municipio del área metropolitana.

    Guarda su nombre y administra la lista de localidades que pertenecen a él.
    """
    def __init__(self, el_nombre):
        """
        Guarda el nombre del municipio e inicializa la lista de localidades vacía.

        Parametros:
        - el_nombre (str): Nombre del municipio.
        """
        self.nombre = el_nombre
        self.localidades = []

    def __str__(self):
        """
        Devuelve un texto sencillo con el nombre del municipio y la cantidad 
        de localidades que contiene.

        Retorna:
        - str: Texto con el nombre y total de localidades.
        """
        return(f"Municipio:{self.nombre} y sus localidades {len(self.localidades)}")


    def agregar_localidad(self, la_localidad):
        """
        Añade un objeto Localidad a la lista de localidades del municipio.

        Parametros:
        - la_localidad (Localidad): La localidad que se va a guardar.
        """
        self.localidades.append(la_localidad)


    def localidades_con_coordenadas(self):
        """
        Filtra y guarda en una lista solo las localidades del municipio 
        que tienen coordenadas geograficas validas.

        Retorna:
        - list: Lista de objetos Localidad que poseen latitud y longitud.
        """
        validas = []
        for loc in self.localidades:
            if loc.tiene_coordenadas():
                validas.append(loc)
        return validas
    

    def reporte_inicial(self):
        """Esta funcion debe imprimir por el municipio la cantidad de localidades cargadas,
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
        """Esta funcion debe mostrar la lista de localidades con su indice, de manera que el usuario ingrese el que quiera consultar"""
        localidades_validas = self.localidades_con_coordenadas()

        if len(localidades_validas) == 0:
            print("Este municipio no posee localidades que tengan coordenadas validas. Disculpe!")
        else:
            print(f"---------------------------------------------------------------------------------\nLocalidades de {self.nombre}\n---------------------------------------------------------------------------------")
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

