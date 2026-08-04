from Municipio import Municipio
from Localidad import Localidad
from Clima_Actual import Clima_Actual
from RegistroHistorico import RegistroHistorico

import json
import matplotlib.pyplot as plt
import requests
import estadisticas
import pandas as pd

URL_REAL = "https://api.open-meteo.com/v1/forecast" #API para datos en tiempo real
URL_HISTORICO = "https://archive-api.open-meteo.com/v1/archive" #API para datos historicos


class SistemaMeteo:
    def __init__(self, la_ruta_json):
        self.ruta_json = la_ruta_json
        self.municipios = []
        self.consultas = []

        self.cargar_datos()


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


    def validar_fecha(self, fecha):
        #primero validamos que el formato sea el correcto
        lista_fecha = fecha.split("-")

        if len(lista_fecha) != 3:
            print("Recuerda utilizar '-' para separar, el formato es (AAAA-MM-DD) (anio, mes, dia). Intenta otra vez")
            return False

        elif len(lista_fecha) == 3:
            anio = lista_fecha[0] 
            mes = lista_fecha[1] 
            dia = lista_fecha[2] 
            
            if anio.isdigit() == True and mes.isdigit() == True and dia.isdigit() == True:
                
                if len(anio) == 4 and len(mes) == 2 and len(dia) == 2:
                    #validamos que la fecha exista, #errors = "coerce" nos devuelve un dato nulo si la fecha no existe
                    fecha_pd = pd.to_datetime(fecha, errors= "coerce")
                    if pd.isna(fecha_pd) == True:
                        print("La fecha que ingresaste no existe. Prueba otra vez.")
                        return False 
                    else:
                        #Comprobamos si la fecha es menor a la de hoy con 5 dias de diferencia o mayor al 1-01-1940 porque son los limites de la API-OPENMETEO
                        limite_minimo = pd.to_datetime("1940-01-01")
                        limite_maximo = pd.to_datetime("today") - pd.Timedelta(days=5)

                        if fecha_pd >= limite_minimo and fecha_pd <= limite_maximo:
                            return True
                        #Si la fecha se encuentra dentro de los rangos devolvemos True 
                        else:
                            print("Nuestros registros llegan desde el 1940-01-01 hasta 5 dias atras, fecha fuera de rango.") 
                            return False
                              
                else: 
                    print("Longitud de datos incorrecta, el formato es (AAAA-MM-DD) (anio, mes, dia). Intenta otra vez")
                    return False
            else: 
                print("Recuerda utilizar '-' para separar, el formato es (AAAA-MM-DD) (anio, mes, dia) y sin letras. Intenta otra vez")
                return False

    def fecha_menor(self, fecha1, fecha2):
        fecha1_pd = pd.to_datetime(fecha1)
        fecha2_pd = pd.to_datetime(fecha2)

        if fecha1_pd < fecha2_pd:
            return True 
        else:
            return False



        
            

  
        

