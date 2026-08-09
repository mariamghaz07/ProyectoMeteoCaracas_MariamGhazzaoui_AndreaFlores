import matplotlib.pyplot as plt

class RegistroHistorico:
    """
    Clase que representa el reporte del clima historico de una localidad.

    Permite agrupar los datos de temperatura, humedad, precipitacion acumulada y viento por mes, calcular sus valores
    promedio y generar una grafica con su evolucion anual.
    """
    def __init__ (self, la_localidad, las_fechas, las_temperaturas, las_humedades, las_precipitaciones, los_vientos):
        """
        Guarda los datos del clima historico recibidos para la localidad.

        Parametros:
        - la_localidad (Localidad): Objeto con la informacion de la localidad.
        - las_fechas (list): Lista de cadenas con las fechas en formato AAAA-MM-DD.
        - las_temperaturas (list): Lista de temperaturas registradas en grados Celsius (°C).
        - las_humedades (list): Lista de porcentajes de humedad relativa registrados (%).
        - las_precipitaciones (list): Lista de precipitacion acumulada registrados (%).
        - los_vientos (list): Lista de velocidades de viento registrados (%).

        """
        self.localidad = la_localidad
        self.fechas = las_fechas
        self.temperaturas = las_temperaturas
        self.humedades = las_humedades
        self.precipitaciones = las_precipitaciones
        self.vientos = los_vientos
    def __str__(self):
        """Genera un texto informativo con el nombre de la localidad y los registros guardados
        Retorna:
        - str: Cadena formateada con la localidad y la cantidad de registros."""
        return f"Historico de {self.localidad.nombre} ({len(self.fechas)} registros diarios guardados)"
    
    def desglose_mensual(self):
        """Agrupa los datos diarios de manera mensual e imprime la informacion detalladamente
        Calcula la temperatura, humedad, precipitacion acumulada y velocidad de viento promedios para cada mes, 
        finaliza con los promedios generales de la consulta"""
        #Generamos una lista de los meses que estan presentes en la consulta
        if not self.fechas:
            print("No tenemos los registros")
            return
        meses = []
        for fecha in self.fechas:
            mes = fecha[:7]
            if mes in meses:
                continue
            else:
                meses.append(mes)
        #debemos mostrar entonces los promedios por cada mes de la consulta
        print("-------------------- DATOS CLIMATICOS POR MES --------------------")

        for mes in meses:
            temperaturas = []
            humedades = []
            precipitaciones = []
            vientos = []
            
            print()
            print(f"Para el mes {mes}")
            for i in range(len(self.fechas)):
                if mes in self.fechas[i]:
                    temperaturas.append(self.temperaturas[i])
                    humedades.append(self.humedades[i])
                    precipitaciones.append(self.precipitaciones[i])
                    vientos.append(self.vientos[i])
                    #calculamos cada magnitud mensualmente y validamos que cada mes tenga datos para no dividir entre 0 por error
            if len(temperaturas) != 0:
                temp_mensual = round(sum(temperaturas)/len(temperaturas), 2)
            if len(humedades) != 0:
                humedad_mensual = round(sum(humedades)/len(humedades), 2)
            if len(precipitaciones) != 0:
                precipitacion_mensual = round(sum(precipitaciones), 2)
            if len(vientos) != 0:
                viento_mensual = round(sum(vientos)/len(vientos), 2)

            #imprimimos cada una en pantalla
            print(f"\nTemperatura: {temp_mensual}°C.\nHumedad relativa: {humedad_mensual}%\nPrecipitacion acumulada: {precipitacion_mensual}mm\nVelocidad del viento: {viento_mensual}km/hr\n--------------------------------------------------------------------------")
        print(f"VALORES PROMEDIO DE CADA MAGNITUD:\n\nPromedio de temperatura: {round(sum(self.temperaturas)/len(self.fechas), 2)}°C\nPromedio de humedad relativa: {round(sum(self.humedades)/len(self.fechas), 2)}%\nPromedio de precipitacion acumulada: {round(sum(self.precipitaciones)/len(meses), 2)}mm\nPromedio de vientos: {round(sum(self.vientos)/len(self.fechas), 2)}km/hr\n")

    def generar_grafica_historica(self):
        """Genera y muestra una grafica de lineas multivariable que representa cada magnitud climatica.
        Calcula los promedios anuales y dibuja las variables en pantalla utilizando una escala logaritmica 
        para mantener la legibilidad de los datos"""
        #vamos a agrupar los datos por anio
        anios = []
        temperaturas_xanio = []
        humedades_xanio = []
        precipitaciones_xanio = []
        vientos_xanio = []
        for fecha in self.fechas:
            anio = fecha[:4]
            if anio in anios:
                continue
            else:
                anios.append(anio)

        for anio in anios:
            temperaturas = []
            humedades = []
            precipitaciones = []
            vientos = []
            for i in range(len(self.fechas)):
                if anio in self.fechas[i]:
                    temperaturas.append(self.temperaturas[i])
                    humedades.append(self.humedades[i])
                    precipitaciones.append(self.precipitaciones[i])
                    vientos.append(self.vientos[i])
            #calculamos cada promedio y las agregamos a una lista para poder graficarlas
            if len(temperaturas) != 0:
                promedio_temp = round(sum(temperaturas)/len(temperaturas), 2)
                temperaturas_xanio.append(promedio_temp)
            if len(humedades) != 0:
                promedio_humedades = round(sum(humedades)/len(humedades), 2)
                humedades_xanio.append(promedio_humedades)
            if len(precipitaciones) != 0:
                promedio_precipitaciones = round(sum(precipitaciones), 2)
                precipitaciones_xanio.append(promedio_precipitaciones)
            if len(vientos) != 0:
                promedio_vientos = round(sum(vientos)/len(vientos), 2)
                vientos_xanio.append(promedio_vientos)
        #generamos la grafica usando matplotlib
        #Asignamos cada yn a una lista de promedios de la magnitud especifica
        x1 = anios
        y1 = temperaturas_xanio

        y2 = humedades_xanio

        y3 = precipitaciones_xanio

        y4 = vientos_xanio

        fig, ax = plt.subplots()
        
        plt.plot(x1 , y1, marker = "o", color = "red", label = "Temperatura Anual (°C)" )
        plt.plot(x1 , y2, marker = "o", color = "blue", label = "Humedad Relativa Anual (%)" )
        plt.plot(x1 , y3, marker = "o", color = "green", label = "Precipitacion Anual (mm)")
        plt.plot(x1 , y4, marker = "o", color = "orange", label = "Velocidad del viento anual (km/hr)")

        plt.title(f"Evolucion del Clima - {self.localidad.nombre}")

        plt.xlabel("Anios consultados")
        plt.legend()
        #se aplica escala logaritmica en y para que se puedan apreciar las magnitudes diferentes a la precipitacion, ya que sus valores eran muy grandes en comparacion
        plt.yscale('log')

        plt.show()
        
 



            
        
        
        