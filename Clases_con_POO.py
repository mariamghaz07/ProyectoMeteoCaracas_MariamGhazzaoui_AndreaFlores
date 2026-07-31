import json
import matplotlib.pyplot as plt
import requests
import estadisticas

#Estos son los archicos que vamos a necesitar para las ultimas 2 clases

#URL'S de la API Open-Meteo

URL_REAL = "https://api.open-meteo.com/v1/forecast" #API para datos en tiempo real
URL_HISTORICO = "https://archive-api.open-meteo.com/v1/archive" #API para datos historicos

class Localidad:
    #Creamos la primera clase que es la localidad, en donde se mostrara el area geografica del area metropolitano
    def __init__(self, el_nombre, la_latitud=None, la_longitud=None):
        self.nombre = el_nombre
        self.latitud = la_latitud
        self.longitud = la_longitud
    #Se le pone las atribuciones correspondiente y se clasifican cada una, con su nombre y sus coordenada geograficas
    #Como hay algunas que no tienen latitud ni longitud se clasifica como "None"
    def __str__(self):
        return f"Localidad: {self.nombre}, Latitud: {self.latitud}, Longitud: {self.longitud}"
    #Aqui se mostrata en pantalla toda la informacion de la localidad
    def tiene_coordenadas(self):
        return self.latitud is not None and self.longitud is not None 
    #Se hace un bool para comprobar si tiene o no coordenada, ya que hay algunas que si la tienen 
    #Esto permitira si se coloca sus coordenadas o no

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
            porcentaje_localidades_coordenadas = (localidades_coordenadas / localidades_totales) * 100
        else:
            porcentaje_localidades_coordenadas = 0
        #para mostrarlo en pantalla
        print(f"Para el municipio {self.nombre}, se han cargado {localidades_totales} localidades.\n {localidades_coordenadas} tienen coordenadas y {localidades_sin_coordenadas} no tienen\nPorcentaje: {porcentaje_localidades_coordenadas}%")

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
                        print("Selecciona una localidad dentro del rango, por favor usa numeros.")
                    else: 
                        seguir = False
                        return localidades_validas[opcion - 1]
                else:
                    print("No ingreses letras ni simbolos, por favor.")

class Clima_Actual:
#Aqui tenemos la clase en donde nos mostraran el clima de cada localidad
    def __init__(self, la_localidad, la_temperatura, la_humedad, la_velocidad_viento, el_codigo_tiempo):
        self.localidad = la_localidad
        self.temperatura = la_temperatura
        self.humedad = la_humedad
        self.velocidad_viento = la_velocidad_viento
        self.codigo_tiempo = el_codigo_tiempo
    #Este es el reporte recibido del clima por cada localidad
    def __str__(self):
        estado = self.traducir_codigo_tiempo()
    #Se creo esta variable para poder determinar mejor el tiempo de cada localidad (lluvioso, soleado, despejado, etc..)
        return (f"{self.localidad.nombre}/n Coordenadas: {self.localidad.latitud}, {self.localidad.longitud}/n Temperatura: {self.temperatura}°C /n Humedad: {self.humedad}% /n Viento: {self.velocidad_viento}km/h /n Estado del tiempo: {estado} ")
    #Aqui se mostraran los datos meteorologicos de cada localidad
    def traducir_codigo_tiempo(self):
    #Aqui se determinara el tiempo de cada localidad segun el numero que contenga
        if self.codigo_tiempo ==0:
            return "Despejado"
        elif self.codigo_tiempo in [1, 2, 3]:
            return "Nublado"
        elif self.codigo_tiempo in [51, 61, 63, 80]:
            return "Lluvia"
        else:
            return "Variable/Desconocido"
class RegistroHistorico:
    def __init__ (self, la_localidad, las_fechas, las_temperaturas, las_humedades, las_precipitaciones, los_vientos):
        self.localidad = la_localidad
        self.fechas = las_fechas
        self.temperaturas = las_temperaturas
        self.humedades = las_humedades
        self.precipitaciones = las_precipitaciones
        self.vientos = los_vientos
    def __str__(self):
        return "f Historico de {self.localidad.nombre} ({len(self.fechas)} registros guardados)"
    def mostrar_caluroso_frio(self):
        pass
    def calcular_promedio(self):
        pass
    def generar_graficos(self):
        pass

class SistemaMeteo:
    def __init__(self, la_ruta_json):
        self.ruta_json = la_ruta_json
        self.municipios = []
        self.consultas = []
    def __str__(self):
        return f"Sistema MeteoCaracas: {len(self.municipios)} municipios"
    def agregar_municipio (self, el_municipio):
        self.municipios.append(el_municipio)
    def guardar_consulta(self, la_consulta_clima):
        self.consultas.append(la_consulta_clima)
    def cargar_datos(self):
        #Cargamos el archivo de localidades 
        with open(self.ruta_json, encoding="utf-8") as info:
            datos_json = json.load(info)
        """Se le especifica a la lectura del archivo json la codificacion "utf-8" para evitar conflictos
        de lectura con caracteres especiales como acentos u "ñ" """
        for datos_municipio in datos_json:
            mun_nuevo = Municipio(datos_municipio)
            localidades_lista = datos_json[datos_municipio]
            for loc in localidades_lista:
                loc_nueva = Localidad(loc["localidad"], loc["latitud"], loc["longitud"])
                mun_nuevo.agregar_localidad(loc_nueva)
            self.municipios.append(mun_nuevo)
    
    def reporte_inicial_total(self):
        """se encarga de mostrar el reporte de las localidades en cada uno de los municipios cargados"""
        print('-----------------------------------------------------------------------------------------------------------')
        print("                               CARGA INICIAL DE SISTEMA METEO")
        print('-----------------------------------------------------------------------------------------------------------')
        for municipio in self.municipios:
            municipio.reporte_inicial()
            print('-----------------------------------------------------------------------------------------------------------')

    def seleccionar_municipio(self):
        """esta funcion debe mostrar la lista de municipios con su indice, de manera que el usuario ingrese el que quiera consultar"""
        for i, mun in enumerate(self.municipios):
            print(f"{i + 1}- {mun.nombre}")
        
        """debe buscar la opcion elegida por el usuario y retornar el municipio que quiere consultar"""
        seguir = True
        while seguir:
            opcion = (input("Ingresa el municipio que quieras consultar: "))
            #Comprueba si la opcion es numerica antes de entrar a los condicionales 
            if opcion.isdigit() == True:
                opcion = int(opcion)
                    #Comprueba y devuelve el municipio elegido
                if opcion > len(self.municipios) or opcion <= 0:
                    print("Selecciona un municipio dentro del rango, por favor.")
                else: 
                    seguir = False
                    return self.municipios[opcion - 1]
            else:
                print("No ingreses letras ni simbolos, por favor.")
    
    def consultar_clima_actual(self, localidad):
        """va a recibir la localidad elegida, consultar a la api y crear un objeto de tipo Clima_Actual"""
        
        informacion_api = {
        "latitude": localidad.latitud,
        "longitude": localidad.longitud,
        "current": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m", "weather_code"]
    }
    
    #esto accede a internet y busca la informacion que necesitamos consultar en la longitud y latitud del objeto Localidad que le estamos pasando
        respuesta = requests.get(URL_REAL, params=informacion_api) 
    #esto accede a la temperatura, humedad, velocidad de =l viento, etc... Esta en forma de diccionario que asignamos a "clima"
        clima = respuesta.json()["current"] 
    #accedemos a cada uno de los parametros y se los asignamos a una variable
        temperatura = clima["temperature_2m"]
        humedad = clima["relative_humidity_2m"]
        velocidad_viento= clima["wind_speed_10m"]
        codigo_clima = clima["weather_code"]
    
    #creamos el objeto de tipo Clima_Actual
        clima_nuevo = Clima_Actual(localidad, temperatura, humedad, velocidad_viento, codigo_clima)

        self.guardar_consulta(clima_nuevo)
        return clima_nuevo

    def consultar_clima_historico(self, localidad, inicio, final):
        """va a recibir la localidad elegida, consultar a la api y crear un objeto de tipo RegistroHistorico"""

        informacion_historica_api = {
            "latitude": localidad.latitud,
            "longitude": localidad.longitud,
            "start_date": inicio,
            "end_date": final,
            "daily": ["temperature_2m_max", "relative_humidity_2m_mean", "precipitation_sum", "wind_speed_10m_max"]
        }

        #accedemos a la informacion de la api
        response = requests.get(URL_HISTORICO, params= informacion_historica_api)
        #nos interesa la informacion diaria de temperatura, humedad, etc. Por eso accedemos a "daily"
        clima_historico = response.json()["daily"]

        #asignamos cada parametro obtenido a una variable y creamos el objeto de tipo RegistroHistorico
        fechas = clima_historico["time"]
        temperatura = clima_historico["temperature_2m_max"]
        humedad = clima_historico["relative_humidity_2m_mean"]
        precipitacion = clima_historico["precipitation_sum"]
        velocidad_viento = clima_historico["wind_speed_10m_max"]

        return RegistroHistorico(localidad, fechas, temperatura, humedad, precipitacion, velocidad_viento)


       

            



    
