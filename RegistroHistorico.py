

class RegistroHistorico:
    def __init__ (self, la_localidad, las_fechas, las_temperaturas, las_humedades, las_precipitaciones, los_vientos):
        self.localidad = la_localidad
        self.fechas = las_fechas
        self.temperaturas = las_temperaturas
        self.humedades = las_humedades
        self.precipitaciones = las_precipitaciones
        self.vientos = los_vientos
    def __str__(self):
        return f"Historico de {self.localidad.nombre} ({len(self.fechas)} registros guardados)"
    