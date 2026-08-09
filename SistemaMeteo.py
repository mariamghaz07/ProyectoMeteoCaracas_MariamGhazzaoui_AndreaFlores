from datetime import datetime, date, timedelta
from Municipio import Municipio
from Localidad import Localidad
from Clima_Actual import Clima_Actual
from RegistroHistorico import RegistroHistorico

import json
import matplotlib.pyplot as plt
import requests

URL_REAL = "https://api.open-meteo.com/v1/forecast" # API para datos en tiempo real
URL_HISTORICO = "https://archive-api.open-meteo.com/v1/archive" # API para datos historicos


class SistemaMeteo:
    def __init__(self, la_ruta_json):
        self.ruta_json = la_ruta_json
        self.municipios = []
        self.consultas = []

        self.cargar_datos()

    def __str__(self):
        return f"Sistema MeteoCaracas: {len(self.municipios)} municipios"

    def guardar_consulta(self, la_consulta_clima):
        self.consultas.append(la_consulta_clima)

    def cargar_datos(self):
        # Cargamos el archivo de localidades 
        with open(self.ruta_json, encoding="utf-8") as info:
            datos_json = json.load(info)
        """Se le especifica a la lectura del archivo json la codificacion "utf-8" para evitar conflictos
        de lectura con caracteres especiales como acentos u "ñ" """
        for municipio in datos_json:
            mun_nuevo = Municipio(municipio)
            localidades_lista = datos_json[municipio]
            for loc in localidades_lista:
                loc_nueva = Localidad(loc["localidad"], municipio, loc["latitud"], loc["longitud"])
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
            # Comprueba si la opcion es numerica antes de entrar a los condicionales 
            if opcion.isdigit() == True:
                opcion = int(opcion)
                # Comprueba y devuelve el municipio elegido
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

        respuesta = requests.get(URL_REAL, params=informacion_api) 
        clima = respuesta.json()["current"] 

        temperatura = clima["temperature_2m"]
        humedad = clima["relative_humidity_2m"]
        velocidad_viento = clima["wind_speed_10m"]
        codigo_clima = clima["weather_code"]

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

        response = requests.get(URL_HISTORICO, params=informacion_historica_api)
        clima_historico = response.json()["daily"]

        fechas = clima_historico["time"]
        temperatura = clima_historico["temperature_2m_max"]
        humedad = clima_historico["relative_humidity_2m_mean"]
        precipitacion = clima_historico["precipitation_sum"]
        velocidad_viento = clima_historico["wind_speed_10m_max"]

        return RegistroHistorico(localidad, fechas, temperatura, humedad, precipitacion, velocidad_viento)

    def validar_fecha(self, fecha):
        # primero validamos que el formato sea el correcto
        lista_fecha = fecha.split("-")

        if len(lista_fecha) != 3:
            print("Recuerda utilizar '-' para separar, el formato es (AAAA-MM-DD) (anio, mes, dia). Intenta otra vez")
            return False

        anio, mes, dia = lista_fecha
        if anio.isdigit() and mes.isdigit() and dia.isdigit():
            if len(anio) == 4 and len(mes) == 2 and len(dia) == 2:
                # Validamos que la fecha exista usando la libreria estandar datetime
                try:
                    fecha_dt = datetime.strptime(fecha, "%Y-%m-%d").date()
                except ValueError:
                    print("La fecha que ingresaste no existe. Prueba otra vez.")
                    return False

                # Comprobamos los limites de la API con datetime/date (libreria estandar)
                limite_minimo = date(1940, 1, 1)
                limite_maximo = date.today() - timedelta(days=5)

                if limite_minimo <= fecha_dt <= limite_maximo:
                    return True
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
        try:
            f1 = datetime.strptime(fecha1, "%Y-%m-%d").date()
            f2 = datetime.strptime(fecha2, "%Y-%m-%d").date()
            return f1 < f2
        except ValueError:
            return False

    def validar_localidad(self, localidad):
        for mun in self.municipios:
            for loc in mun.localidades:
                if localidad.lower().replace(" ", "") == loc.nombre.lower().replace(" ", ""):
                    l = loc
                    if loc.tiene_coordenadas():
                        clima = self.consultar_clima_actual(l)
                        if clima:
                            print("\n" + "=" * 40)
                            print(clima)
                            print("=" * 40)
                            return 
                    else:
                        print("Esa localidad no tiene coordenadas registradas, disculpe.")
                        return 
        print("No se encontro ninguna localidad con ese nombre, intenta de nuevo")
        return 

    def buscar_nombre(self, cadena):
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
                    if cadena[i] != nombre[i]:
                        validado = False
                        break 
                
                if validado:
                    localidades_posibles.append(loc)

        return localidades_posibles
