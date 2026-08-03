

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
        return (f"{self.localidad.nombre}\n Coordenadas: {self.localidad.latitud}, {self.localidad.longitud}\n Temperatura: {self.temperatura}°C \n Humedad: {self.humedad}% \n Viento: {self.velocidad_viento}km/h \n Estado del tiempo: {estado} ")
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