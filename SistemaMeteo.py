from Municipio import Municipio
from Localidad import Localidad
from Clima_Actual import Clima_Actual
from RegistroHistorico import RegistroHistorico

import json
import requests
import pandas as pd

URL_REAL = "https://api.open-meteo.com/v1/forecast" #API para datos en tiempo real
URL_HISTORICO = "https://archive-api.open-meteo.com/v1/archive" #API para datos historicos


class SistemaMeteo:
    """Clase que administra la carga de datos, gestion de municipios y conexion con la API
    Coordina las consultas de clima en tiempo real e histórico, así como el filtrado
    y búsqueda de localidades en el área metropolitana de Caracas.
    """
    def __init__(self, la_ruta_json):
        """Inicia el sistema y carga las localidades desde el archivo JSON.

        Parametros:
        - la_ruta_json (str): Ruta del archivo JSON con los datos.
        """
        self.ruta_json = la_ruta_json
        self.municipios = []
        self.consultas = []

        self.cargar_datos()


    def __str__(self):
        """Devuelve un resumen del sistema indicando la cantidad de municipios cargados.

        Retorna:
        - str: Cadena de texto con el total de municipios almacenados.
        """
        return f"Sistema MeteoCaracas: {len(self.municipios)} municipios"

    def guardar_consulta(self, la_consulta_clima):
        """Guarda una consulta realizada en tiempo real dentro de la lista de consultas.

        Parametros:
        - la_consulta_clima (Clima_Actual): Objeto de consulta a almacenar.
        """
        self.consultas.append(la_consulta_clima)


    def cargar_datos(self):
        """Lee el archivo JSON de Municipio y localidades e instancia objetos de tipo Municipio y Localidad"""
        #Cargamos el archivo de localidades 
        with open(self.ruta_json, encoding="utf-8") as info:
            datos_json = json.load(info)
        #Se le especifica a la lectura del archivo json la codificacion "utf-8" para evitar conflictos
        #de lectura con caracteres especiales como acentos u "ñ" 
        for municipio in datos_json:
            mun_nuevo = Municipio(municipio)
            localidades_lista = datos_json[municipio]
            for loc in localidades_lista:
                loc_nueva = Localidad(loc["localidad"], municipio, loc["latitud"], loc["longitud"])
                mun_nuevo.agregar_localidad(loc_nueva)
            self.municipios.append(mun_nuevo)
    
    def reporte_inicial_total(self):
        """Muestra el reporte de cobertura de localidades para todos los municipios cargados."""
        print('-----------------------------------------------------------------------------------------------------------')
        print("                               CARGA INICIAL DE SISTEMA METEO")
        print('-----------------------------------------------------------------------------------------------------------')
        for municipio in self.municipios:
            municipio.reporte_inicial()
            print('-----------------------------------------------------------------------------------------------------------')

    def seleccionar_municipio(self):
        """Despliega la lista numerada de municipios y solicita al usuario seleccionar uno.

        Retorna:
        - Municipio: El objeto Municipio seleccionado por el usuario.
        """
        #esta funcion debe mostrar la lista de municipios con su indice, de manera que el usuario ingrese el que quiera consultar"""
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
        """Consulta la API de Open-Meteo para obtener el clima en tiempo real de una localidad.

        Parametros:
        - localidad (Localidad): Objeto Localidad con latitud y longitud válidas.

        Retorna:
        - Clima_Actual: Objeto con los datos meteorológicos actuales consultados.
        """
        
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
        """Consulta la API de archivo de Open-Meteo para obtener la informacion climatica historica en un rango de fechas.

        Parametros:
        - localidad (Localidad): Objeto Localidad a consultar.
        - inicio (str): Fecha inicial en formato AAAA-MM-DD.
        - final (str): Fecha final en formato AAAA-MM-DD.

        Retorna:
        - RegistroHistorico: Objeto con las listas de datos diarios obtenidos.
        """
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
        """Comprueba si una cadena representa una fecha válida y dentro del rango de la API.

        Parametros:
        - fecha (str): Cadena de texto con la fecha a comprobar (AAAA-MM-DD).

        Retorna:
        - bool: True si la fecha es válida y está dentro del rango permitido, False en caso contrario.
        """
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
        """Verifica si la primera fecha es menor a la segunda.

        Parametros:
        - fecha1 (str): Primera fecha en formato AAAA-MM-DD.
        - fecha2 (str): Segunda fecha en formato AAAA-MM-DD.

        Retorna:
        - bool: True si fecha1 es menor que fecha2, False en caso contrario."""

        fecha1_pd = pd.to_datetime(fecha1)
        fecha2_pd = pd.to_datetime(fecha2)

        if fecha1_pd < fecha2_pd:
            return True 
        else:
            return False

    def validar_localidad(self, localidad):
        """Busca una localidad por su nombre exacto y consulta su clima si tiene coordenadas válidas.

        Parametros:
        - localidad (str): Nombre de la localidad a validar.
        """
        for mun in self.municipios:
            for loc in mun.localidades:
                if localidad.lower().replace(" ", "") == loc.nombre.lower().replace(" ", ""):
                    l = loc
                    if loc.tiene_coordenadas():
                        clima = self.consultar_clima_actual(l)
                        if clima:
                            print(f"\n{'=' * 40}\n{clima}\n{'=' * 40}")
                            return 
                    else:
                        print("Esa localidad no tiene coordenadas registradas, disculpe.")
                        return 
        print("No se encontro ninguna localidad con ese nombre, intenta de nuevo")
        return 

    def buscar_nombre(self, cadena):
        """Filtra y devuelve las localidades cuyos nombres coincidan o comiencen con la cadena dada.

        Parametros:
        - cadena (str): Texto o fragmento de texto a buscar.

        Retorna:
        - list: Lista de objetos Localidad que coinciden con la búsqueda.
        """
        localidades_posibles = []
        cadena = cadena.lower().replace(" ", "")
        if len(cadena) == 0:
            return []
        for mun in self.municipios:
                for loc in mun.localidades:   
                    if len(cadena) > len(loc.nombre.lower().replace(" ", "")):
                        continue 
                    nombre = loc.nombre.lower().replace(" ", "")
                    validado = True
                    for i in range(len(cadena)):
                        if cadena[i] !=  nombre[i]:
                            validado = False
                            break 
                    
                    if validado:
                        localidades_posibles.append(loc)

        return localidades_posibles

