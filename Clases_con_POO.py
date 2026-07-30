import json
import matplotlib.pyplot as plt
import requests
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
            if loc.tiene_coordenada():
                validas.append(loc)
        return validas
    #Aqui se permitira poner las coordenadas de las localidades que lo posean y sea visible

class Clima_Actual:
#Aqui tenemos la clase en donde nos mostraran el clima de cada localidad
    def __init__(self, la_localidad, la_temperatura, la_humedad, la_velocidad_viento, el_codigo_tiempo):
        self.localidad = la_localidad
        self.temperatura = la_temperatura
        self.humedad = la_humedad
        self.velocidad_viento = la_velocidad_viento
        self.codigo_viento = el_codigo_tiempo
    #Este es el reporte recibido del clima por cada localidad
    def __str__(self):
        estado = self.traducir_codigo_tiempo()
    #Se creo esta variable para poder determinar mejor el tiempo de cada localidad (lluvioso, soleado, despejado, etc..)
        return (f"{self.localidad.nombre}/n Coordenadas: {self.localidad.latitud}, {self.localidad.longitud}/n Temperatura: {self.temperatura}°C /n Humedad: {self.humedad}% /n Viento: {self.velocidad_viento}km/h /n Estado del tiempo: {estado} ")
    #Aqui se mostraran los datos meteorologicos de cada localidad
    def traucir_codigo_tiempo(self):
    #Aqui se determinara el tiempo de cada localidad segun el numero que contenga
        if self.codigo_tiempo ==0:
            return "Despejado"
        elif self.tiempo in [1, 2, 3]:
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
