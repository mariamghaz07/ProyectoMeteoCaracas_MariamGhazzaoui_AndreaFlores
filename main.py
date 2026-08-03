from SistemaMeteo import SistemaMeteo
from Municipio import Municipio
from Localidad import Localidad
from Clima_Actual import Clima_Actual
from RegistroHistorico import RegistroHistorico
import estadisticas


def main():
     sistema = SistemaMeteo("zonas_caracas.json")

     while True:
         print("----Sistema Meteorologico de Caracas----")
         print("1. Ver reporte inicial (Carga de datos)")
         print("2. Consultar clima en tiempo real")
         print("3. Consultar registro historico y datos")
         print("4. Ver las estadisticas de la consulta")
         print("Salir del programa")

         opcion =int(input("Seleccione la opcion de su preferencia: "))

         if opcion == 1:
              print("----Reporte inicial de cobertura----")
              sistema.reporte_inicial_total()
         elif opcion == 2:
              print("----Consulta en tiempo real----")
              municipio = sistema.seleccionar_municipio()
              if municipio:
                   localidad = municipio.seleccionar_localidad()
                   if localidad:
                        clima = sistema.consultar_clima_actual(localidad)
                        if clima:
                             print("\n" + "=" * 40)
                             print(clima)
                             print("=" * 40)
         elif opcion == 3:
              print("----Consulta de datos historicos----")
              municipio = sistema.seleccionar_municipio()
              if municipio:
                   localidad = municipio.seleccionar_localidad()
                   if localidad:
                        inicio = input("Ingrese fecha de inicio (AAAA-MM-DD): ").strip()
                        fin = input("Ingrese fecha de fin (AAAA-MM-DD): ").strip()

                        historico = sistema.consultar_clima_historico(localidad, inicio, fin)
                        if historico:
                             print("/n" + "=" * 40)
                             print(historico)

                             promedio = estadisticas.calcular_promedio_temperatura(historico)
                             print(f"Temperatura promedio del periodo: {round(promedio, 2)}")

                             extremos = estadisticas.obtener_extremos_historicos(historico)
                             if extremos:
                                  print(f"Anio mas caluroso: {extremos['caluroso'][0]} {round(extremos['caluroso'][1], 1)})")
                                  print(f"Anio mas fresco: {extremos['fresco'][0]} ({round(extremos['fresco'][1], 1 )})")
                                  print(f"Anio mas lluvioso: {extremos['lluvioso'][0]} ({round(extremos['lluvioso'][1], 1)})")
                                  print(f"Anio mas humedo: {extremos['humedo'][0]} ({round(extremos['humedo'][1], 1)})")
                             print("=" * 40)

                             estadisticas.generar_grafica_historica(historico)
         elif opcion == 4:
              print("----Ver estadisticas de la consulta----")
              if len(sistema.consultas) == 0:
                   print("Aun no has realizado ninguna consulta en tiempor real")
              else:
                   print(f"Total de consultas realizadas hata ahora:{len(sistema.consultas)} ")

                   for i, c in enumerate(sistema.consultas, 1):
                        print(f"{i}. {c.localidad.nombre} - Temp {c.temperatura}")

                        resumen = estadisticas.calcular_estadisticas(sistema.consultas)
                        if not resumen:
                            print("Aun no has realizado alguna consulta")
                        else:
                            print(f"Total de consultas realizadas: {len(sistema.consultas)}")
                            print(f"Localidad mas calida: {resumen['mas_calida'].localidad.nombre} ({resumen['mas_calida'].temperatura})")
                            print(f"Localidad mas fris: {resumen['mas_fria'].localidad.nombre} ({resumen['mas_fria'].temperatura})")
                            print(f"Promedio de la consulta: {round(resumen['promedio'], 2)}")

         elif opcion == 5:
              print("Gracias por usar el sistema metereologico de Caracas!")
              break
         else:
              print("Opcion invalida. Debe presionar un numero del 1 al 5")

if __name__ == "__main__":
     main()

              
                            
