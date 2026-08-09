

class Clima_Actual:
    """
    Clase que representa el reporte del clima en tiempo real de una localidad.

    Guarda los datos meteorologicos obtenidos de la API (temperatura, humedad,
    viento y codigo del clima) y permite mostrarlos formateados.
    """
    def __init__(self, la_localidad, la_temperatura, la_humedad, la_velocidad_viento, el_codigo_tiempo):
        """
        Guarda los datos del clima actual recibidos para la localidad.

        Parametros:
        - la_localidad (Localidad): Objeto con la informacion de la localidad.
        - la_temperatura (float): Temperatura actual en grados Celsius (°C).
        - la_humedad (int/float): Porcentaje de humedad relativa (%).
        - la_velocidad_viento (float): Velocidad del viento en km/h.
        - el_codigo_tiempo (int): Codigo numerico enviado por la API que indica el estado del tiempo.
        """

        self.localidad = la_localidad
        self.temperatura = la_temperatura
        self.humedad = la_humedad
        self.velocidad_viento = la_velocidad_viento
        self.codigo_tiempo = el_codigo_tiempo



    def __str__(self):
        estado = self.traducir_codigo_tiempo()
        """
        Genera el texto formateado con toda la informacion del clima para imprimir en pantalla.

        Retorna:
        - str: Cadena de texto ordenada con el municipio, localidad, coordenadas y variables climaticas.
        """
        
        return (f"Municipio: {self.localidad.municipio}\nLocalidad: {self.localidad.nombre}\nCoordenadas: {self.localidad.latitud}, {self.localidad.longitud}\nTemperatura: {self.temperatura}°C \nHumedad: {self.humedad}% \nViento: {self.velocidad_viento}km/h \nEstado del tiempo: {estado} ")



    def traducir_codigo_tiempo(self):
        """
        Convierte el codigo numerico del tiempo recibo de la API a una palabra comprensible.

        Retorna:
        - str: Texto descriptivo del clima ('Despejado', 'Nublado', 'Lluvia' o 'Variable/Desconocido').
        """

        if self.codigo_tiempo ==0:
            return "Despejado"
        elif self.codigo_tiempo in [1, 2, 3]:
            return "Nublado"
        elif self.codigo_tiempo in [51, 61, 63, 80]:
            return "Lluvia"
        else:
            return "Variable/Desconocido"