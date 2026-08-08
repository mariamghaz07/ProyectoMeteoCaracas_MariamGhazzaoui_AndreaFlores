from SistemaMeteo import SistemaMeteo
from Estadisticas import Estadisticas

class App:     
     def __init__(self):
          self.sistema = SistemaMeteo("zonas_caracas.json")
          self.estadisticas = Estadisticas()
     def menu(self):

          while True:
               print()
               print("----Sistema Meteorologico de Caracas----")
               print("1. Ver reporte inicial (Carga de datos)")
               print("2. Consultar clima en tiempo real")
               print("3. Consultar registro historico y datos")
               print("4. Ver las estadisticas de la consulta")
               print("5. Salir del programa")
               print()

               opcion =(input("Seleccione la opcion de su preferencia: "))
               opcion = opcion.strip()

               if opcion in ("1", "2", "3", "4", "5"):
                    opcion = int(opcion)
               
                    if opcion == 1:
                         print()
                         print("----Reporte inicial de cobertura----")
                         self.sistema.reporte_inicial_total()

                    elif opcion == 2:
                         print("----Consulta en tiempo real----")
                         res = input("Presiona (1) para buscar por lista o (2) para buscar por nombre: ")
                         res = res.strip()

                         if res == "1" or res == "2":
                              res = int(res)
                              if res == 1:
                                   print("----Lista de Municipios----")
                                   municipio = self.sistema.seleccionar_municipio()
                                   if municipio:
                                        localidad = municipio.seleccionar_localidad()
                                        if localidad:
                                             clima = self.sistema.consultar_clima_actual(localidad)
                                             if clima:
                                                  print("\n" + "=" * 40)
                                                  print(clima)
                                                  print("=" * 40)
                              elif res == 2:
                                   print("----INICIANDO SISTEMA DE BUSQUEDA POR NOMBRE----")
                                   cond = (input("Presiona (1) para escribir el nombre de la localidad y (2) para escribir solo una parte: ")).strip()
                                   if cond == "1":
                                        loc = input("Ingresa el nombre COMPLETO de la localidad: ")
                                        self.sistema.validar_localidad(loc)
                                   elif cond == "2":
                                        loc = input("Ingresa una parte del nombre de la localidad: ")
                                        localidades_posibles = self.sistema.buscar_nombre(loc)
                                        if not localidades_posibles:
                                             print("No tenemos registros de localidades con ese nombre, intente de nuevo.")
                                        else: 
                                             for i, localidad in enumerate(localidades_posibles):
                                                  print(f"{i +1}- {localidad}")
                                             des = input("Ingresa la localidad a consultar por su indice: ")
                                             if des.isdigit() == True:
                                                  des = int(des)
                                                  if des <= 0 or des > len(localidades_posibles):
                                                       print("Seleccione una localidad dentro del rango")
                                                  else:
                                                       localidad_final = localidades_posibles[des - 1]
                                                       if localidad_final.tiene_coordenadas():
                                                            clima = self.sistema.consultar_clima_actual(localidad_final)
                                                            if clima:
                                                                 print("\n" + "=" * 40)
                                                                 print(clima)
                                                                 print("=" * 40)
                                                       else:
                                                            print("La localidad que elegiste no tiene coordenadas registradas, elige otra.")
                                             else: 
                                                  print("Solo puedes escibir numeros en este campo")
                                   else: 
                                        print("Las opciones validas en este campo son (1) y (2)") 
                              else:
                                   print("Por favor ingresa (1) o (2) para elegir un metodo de busqueda, intenta de nuevo")

                    elif opcion == 3:
                         print()
                         print("----Consulta de datos historicos----")
                         municipio = self.sistema.seleccionar_municipio()
                         if municipio:
                              localidad = municipio.seleccionar_localidad()
                              if localidad:
                                   while True:
                                        #Pedimos las fechas de inicio  final
                                        print("INSTRUCCIONES: La fecha de inicio no puede ser menor a la de fin, no se admiten fechas menores a 1940-01-01 o superiores a cinco dias atras. Siga el formato correctamente.")
                                        inicio = input("Ingrese fecha de inicio (AAAA-MM-DD): ").strip()
                                        fin = input("Ingrese fecha de fin (AAAA-MM-DD): ").strip()

                                        if self.sistema.validar_fecha(inicio) == True and self.sistema.validar_fecha(fin) == True:
                                             if self.sistema.fecha_menor(inicio, fin) == True: 

                                                  historico = self.sistema.consultar_clima_historico(localidad, inicio, fin)
                                                  if historico:
                                                       print("\n" + "=" * 40)
                                                       print(historico)
                                                       #El sistema debe mostrar por mes temperatura, humedad, precipitacion, velocidad del viento
                                                       #Luego valores promedios de cada magnitud
                                                       historico.desglose_mensual()


                                                       # promedio = estadisticas.calcular_promedio_temperatura(historico)
                                                       # print(f"Temperatura promedio del periodo: {round(promedio, 2)}")

                                                       #La parte de los anios extremos funciona bien 
                                                       extremos = self.estadisticas.obtener_extremos_historicos(historico)
                                                       if extremos:
                                                            print(f"REPORTE ANUAL:")
                                                            print(f"Anio mas caluroso: {extremos['caluroso'][0]} {round(extremos['caluroso'][1], 1)}°C)")
                                                            print(f"Anio mas fresco: {extremos['fresco'][0]} ({round(extremos['fresco'][1], 1 )})°C")
                                                            print(f"Anio mas lluvioso: {extremos['lluvioso'][0]} ({round(extremos['lluvioso'][1], 1)}mm)")
                                                            print(f"Anio mas humedo: {extremos['humedo'][0]} ({round(extremos['humedo'][1], 1)}%)")
                                                       print("=" * 40)

                                                       #la grafica debe mostrar el promedio de cada magnitud y aqui solo muestra temperatura
                                                       historico.generar_grafica_historica()
                                                       break
                                             else:
                                                  print("Las fecha de inicio no puede ser mayor que la fecha de fin, tampoco pueden ser iguales. Intenta otra vez")
                                                  break   
                                        else:
                                             break
                                        
                    elif opcion == 4:
                         print()
                         while True:
                              print("----Ver estadisticas de la consulta----")
                              opcion = input("1- Ranking y promedio general de temperatura\n2- Mostrar localidades sin coordenadas")
                              if opcion == "2":
                                        print("--------------MOSTRANDO LOCALIDADES SIN COORDENADAS----------------")
                                        self.estadisticas.mostrar_localidades_sin_coordenadas(self.sistema.municipios)
                                        break
                              
                              elif opcion == "1":
                                   if len(self.sistema.consultas) == 0:
                                        print("Aun no has realizado ninguna consulta en tiempo real")
                                        break
                                   else:     
                                        print(f"Total de consultas realizadas hasta ahora: {len(self.sistema.consultas)} ")

                                        for i, c in enumerate(self.sistema.consultas, 1):
                                             print(f"{i}. {c.localidad.nombre} ({c.localidad.municipio})- Temp {c.temperatura}")
                                        resumen = self.estadisticas.calcular_estadisticas(self.sistema.consultas)
                                        if not resumen:
                                             print("Aun no has realizado alguna consulta")
                                             break
                                        else:
                                             print(f"Localidad mas calida: {resumen['mas_calida'].localidad.nombre} (Municipio {resumen['mas_calida'].localidad.municipio}): ({resumen['mas_calida'].temperatura}°C)")
                                             print(f"Localidad mas fria: {resumen['mas_fria'].localidad.nombre} (Municipio {resumen['mas_fria'].localidad.municipio}): ({resumen['mas_fria'].temperatura}°C)")
                                             print(f"Promedio de la consulta: {round(resumen['promedio'], 2)}°C")
                                             break
                              else:
                                   print("Solo puedes ingresar '1' o '2' en este campo")

                    elif opcion == 5:
                         print("Gracias por usar el sistema metereologico de Caracas!")
                         break
               else:
                    print("Opcion invalida, debe presionar un numero del 1 al 5. Intente otra vez.")
                    


              
                            
