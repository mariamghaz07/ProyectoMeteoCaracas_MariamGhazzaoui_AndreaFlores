

class RegistroHistorico:
    def __init__ (self, la_localidad, las_fechas, las_temperaturas, las_humedades, las_precipitaciones, los_vientos):
        self.localidad = la_localidad
        self.fechas = las_fechas
        self.temperaturas = las_temperaturas
        self.humedades = las_humedades
        self.precipitaciones = las_precipitaciones
        self.vientos = los_vientos
    def __str__(self):
        return f"Historico de {self.localidad.nombre} ({len(self.fechas)} registros diarios guardados)"
    
    def desglose_mensual(self):
        """esta funcion debe agrupar los datos del registro historico en forma mensual e imprimir los datos por mes y los valores promedio"""
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
            print()
            print(f"Temperatura: {temp_mensual}°C.")
            print(f"Humedad relativa: {humedad_mensual}%")
            print(f"Precipitacion acumulada: {precipitacion_mensual}mm")
            print(f"Velocidad del viento: {viento_mensual}km/hr")
            print("--------------------------------------------------------------------------")
        print(f"VALORES PROMEDIO DE CADA MAGNITUD: ")
        print()
        print(f"Promedio de temperatura: {round(sum(self.temperaturas)/len(self.fechas), 2)}°C")
        print(f"Promedio de humedad relativa: {round(sum(self.humedades)/len(self.fechas), 2)}%")
        print(f"Promedio de precipitacion acumulada: {round(sum(self.precipitaciones)/len(meses), 2)}mm")
        print(f"Promedio de vientos: {round(sum(self.vientos)/len(self.fechas), 2)}km/hr")
        print()
        
 



            
        
        
        