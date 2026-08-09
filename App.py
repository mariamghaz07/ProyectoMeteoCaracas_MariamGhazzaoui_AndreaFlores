from SistemaMeteo import SistemaMeteo
from Estadisticas import Estadisticas
import Validaciones

class App:     
    def __init__(self):
        self.sistema = SistemaMeteo("zonas_caracas.json")
        self.estadisticas = Estadisticas()

    def menu(self):
        while True:
            print("""
----Sistema Meteorologico de Caracas----
1. Ver reporte inicial (Carga de datos)
2. Consultar clima en tiempo real
3. Consultar registro historico y datos
4. Ver las estadisticas de la consulta
5. Salir del programa
""")

            opcion = Validaciones.pedir_opcion_menu("Seleccione la opcion de su preferencia: ", 1, 5)

            if opcion == 1:
                print("----Reporte inicial de cobertura----")
                self.sistema.reporte_inicial_total()

            elif opcion == 2:
                res = Validaciones.pedir_opcion_menu("\n----Consulta en tiempo real----\nPresiona (1) para buscar por lista o (2) para buscar por nombre: ", 1, 2)

                localidad = None
                if res == 1:
                    print("----Lista de Municipios----")
                    municipio = self.sistema.seleccionar_municipio()
                    if municipio:
                        localidad = municipio.seleccionar_localidad()
                else:
                    localidad = Validaciones.pedir_localidad_por_nombre(self.sistema)

                if localidad:
                    clima = self.sistema.consultar_clima_actual(localidad)
                    if clima:
                        print(f"\n{'=' * 40}\n{clima}\n{'=' * 40}")

            elif opcion == 3:
                print("\n----Consulta de datos historicos----")
                municipio = self.sistema.seleccionar_municipio()
                if municipio:
                    localidad = municipio.seleccionar_localidad()
                    if localidad:
                        print("INSTRUCCIONES: La fecha de inicio no puede ser mayor a la de fin, no se admiten fechas menores a 1940-01-01 o superiores a cinco dias atras. Siga el formato correctamente.")
                        inicio, fin = Validaciones.pedir_rango_fechas()

                        historico = self.sistema.consultar_clima_historico(localidad, inicio, fin)
                        if historico:
                            print("\n" + "=" * 40)
                            print(historico)
                            historico.desglose_mensual()

                            extremos = self.estadisticas.obtener_extremos_historicos(historico)
                            if extremos:
                                print(
                                    f"REPORTE ANUAL:\n"
                                    f"Anio mas caluroso: {extremos['caluroso'][0]} ({round(extremos['caluroso'][1], 1)}°C)\n"
                                    f"Anio mas fresco: {extremos['fresco'][0]} ({round(extremos['fresco'][1], 1)}°C)\n"
                                    f"Anio mas lluvioso: {extremos['lluvioso'][0]} ({round(extremos['lluvioso'][1], 1)}mm)\n"
                                    f"Anio mas humedo: {extremos['humedo'][0]} ({round(extremos['humedo'][1], 1)}%)"
                                )
                            print("=" * 40)
                            historico.generar_grafica_historica()

            elif opcion == 4:
                opcion_est = Validaciones.pedir_opcion_menu("\n----Ver estadisticas de la consulta----\n1- Ranking y promedio general de temperatura\n2- Mostrar localidades sin coordenadas\nSeleccione una opcion: ", 1, 2)
                
                if opcion_est == 2:
                    print("--------------MOSTRANDO LOCALIDADES SIN COORDENADAS----------------")
                    self.estadisticas.mostrar_localidades_sin_coordenadas(self.sistema.municipios)

                elif opcion_est == 1:
                    Validaciones.validar_y_mostrar_estadisticas_consultas(self.sistema.consultas, self.estadisticas)

            elif opcion == 5:
                print("Gracias por usar el sistema metereologico de Caracas!")
                break