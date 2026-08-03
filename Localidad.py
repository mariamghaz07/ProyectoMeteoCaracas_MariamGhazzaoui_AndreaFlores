
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