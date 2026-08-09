
class Localidad:
    """
    Clase que representa una localidad o zona del área metropolitana.

    Guarda su nombre, el municipio al que pertenece y sus coordenadas 
    geográficas si las tiene disponibles.
    """

    def __init__(self, el_nombre, el_municipio, la_latitud=None, la_longitud=None):
        """
        Guarda la información basica de la localidad al crearla.

        Parametros:
        - el_nombre (str): Nombre de la localidad o sector.
        - el_municipio (str): Nombre del municipio al que pertenece.
        - la_latitud (float/None): Latitud geográfica (por defecto es None si no tiene).
        - la_longitud (float/None): Longitud geográfica (por defecto es None si no tiene).
        """

        self.nombre = el_nombre
        self.municipio = el_municipio
        self.latitud = la_latitud
        self.longitud = la_longitud
    def __str__(self):
        """
        Devuelve una cadena de texto ordenada con todos los datos de la localidad
        para mostrar en pantalla.

        Retorna:
        - str: Texto con municipio, localidad, latitud y longitud.
        """

        return f"Municipio: {self.municipio}, Localidad: {self.nombre}, Latitud: {self.latitud}, Longitud: {self.longitud}"
    def tiene_coordenadas(self):
        """
        Verifica si la localidad tiene registradas coordenadas de latitud y longitud.

        Retorna:
        - bool: True si tiene ambas coordenadas, False si alguna es None.
        """
        return self.latitud is not None and self.longitud is not None 