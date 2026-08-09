import pandas as pd


class Validaciones:
    """
    Clase encargada de validar las entradas del usuario por consola.
    """

    def __init__(self):
        """
        Inicializa la clase de Validaciones.
        """
        pass

    def pedir_opcion_menu(self, mensaje, min_val=1, max_val=5):
        """
        Solicita un numero entero y valida que este dentro del rango especificado.
        """
        seguir = True
        while seguir:
            opcion = input(mensaje).strip()

            if opcion.isdigit() == True:
                opcion = int(opcion)
                if opcion >= min_val and opcion <= max_val:
                    return opcion
                else:
                    print(f"\nSelecciona una opcion dentro del rango ({min_val} a {max_val}), por favor.")
            else:
                print("\nNo ingreses letras ni simbolos, por favor.")

    def pedir_fecha_valida(self, mensaje):
        """
        Solicita una fecha, valida que tenga el formato AAAA-MM-DD, que sea una fecha real
        y que se encuentre dentro del rango permitido por la API.
        """
        seguir = True
        while seguir:
            fecha = input(mensaje).strip()
            lista_fecha = fecha.split("-")

            if len(lista_fecha) != 3:
                print("Recuerda utilizar '-' para separar, el formato es (AAAA-MM-DD) (anio, mes, dia). Intenta otra vez.\n")

            elif len(lista_fecha) == 3:
                anio = lista_fecha[0]
                mes = lista_fecha[1]
                dia = lista_fecha[2]

                if anio.isdigit() == True and mes.isdigit() == True and dia.isdigit() == True:

                    if len(anio) == 4 and len(mes) == 2 and len(dia) == 2:
                        fecha_pd = pd.to_datetime(fecha, errors="coerce")

                        if pd.isna(fecha_pd) == True:
                            print("La fecha que ingresaste no existe. Prueba otra vez.\n")
                        else:
                            limite_minimo = pd.to_datetime("1940-01-01")
                            limite_maximo = pd.to_datetime("today") - pd.Timedelta(days=5)

                            if fecha_pd >= limite_minimo and fecha_pd <= limite_maximo:
                                return fecha
                            else:
                                print("Nuestros registros llegan desde el 1940-01-01 hasta 5 dias atras, fecha fuera de rango.\n")

                    else:
                        print("Longitud de datos incorrecta, el formato es (AAAA-MM-DD) (anio, mes, dia). Intenta otra vez.\n")
                else:
                    print("Recuerda utilizar '-' para separar, el formato es (AAAA-MM-DD) (anio, mes, dia) y sin letras. Intenta otra vez.\n")

    def pedir_rango_fechas(self):
        """
        Solicita la fecha de inicio y de fin, comprobando que la fecha de inicio 
        sea estrictamente menor que la de fin.
        """
        seguir = True
        while seguir:
            inicio = self.pedir_fecha_valida("Ingrese fecha de inicio (AAAA-MM-DD): ")
            fin = self.pedir_fecha_valida("Ingrese fecha de fin (AAAA-MM-DD): ")

            fecha1_pd = pd.to_datetime(inicio)
            fecha2_pd = pd.to_datetime(fin)

            if fecha1_pd < fecha2_pd:
                return inicio, fin
            else:
                print("La fecha de inicio debe ser estrictamente menor a la fecha de fin. Intente de nuevo.\n")

    def pedir_seleccion_lista(self, lista, titulo="Seleccione una opcion: "):
        """
        Muestra una lista numerada y le pide al usuario seleccionar una opcion por su indice.
        """
        for i, item in enumerate(lista):
            print(f"{i + 1}- {item}")

        indice = self.pedir_opcion_menu(titulo, 1, len(lista))
        return lista[indice - 1]

    def pedir_localidad_por_nombre(self, sistema):
        """
        Pide el nombre de una localidad (completo o una parte) y la busca en el sistema.
        Funciona si se ingresa con o sin espacios, mayusculas o minusculas 
        (ej: 'los palos grandes', 'lospalosgrandes', 'la urbina', 'la trinidad').
        """
        print("----INICIANDO SISTEMA DE BUSQUEDA POR NOMBRE----")
        cond = self.pedir_opcion_menu("Presiona (1) para escribir el nombre COMPLETO o (2) para escribir una PARTE: ", 1, 2)

        seguir = True
        while seguir:
            if cond == 1:
                loc = input("Ingresa el nombre COMPLETO de la localidad: ").strip()
                # Se eliminan todos los espacios y se pasa a minusculas
                loc_limpio = loc.lower().replace(" ", "")

                coincidencias = []
                for m in sistema.municipios:
                    for l in m.localidades:
                        # Se eliminan los espacios y minusculas de la localidad guardada para comparar de forma idéntica
                        nombre_guardado = l.nombre.lower().replace(" ", "")
                        if nombre_guardado == loc_limpio:
                            coincidencias.append(l)

                if len(coincidencias) == 0:
                    print("No se encontro ninguna localidad con ese nombre exacto. Intente de nuevo.\n")
                    continue

                localidad = coincidencias[0]

            else:
                loc = input("Ingresa una parte del nombre de la localidad: ").strip()
                # Se eliminan los espacios y se pasa a minusculas la busqueda
                loc_limpio = loc.lower().replace(" ", "")

                posibles = []
                for m in sistema.municipios:
                    for l in m.localidades:
                        nombre_guardado = l.nombre.lower().replace(" ", "")
                        if loc_limpio in nombre_guardado:
                            posibles.append(l)

                if len(posibles) == 0:
                    print("No tenemos registros de localidades con ese nombre, intente de nuevo.\n")
                    continue

                localidad = self.pedir_seleccion_lista(posibles, "Ingresa la localidad a consultar por su indice: ")

            if localidad.tiene_coordenadas() == True:
                return localidad
            else:
                print("La localidad seleccionada no posee coordenadas registradas. Elija otra.\n")

    def pedir_localidad_por_municipio(self, sistema):
        """
        Muestra los municipios y localidades para que el usuario seleccione una.
        """
        seguir = True
        while seguir:
            municipio = sistema.seleccionar_municipio()
            if municipio == None:
                print("No se selecciono un municipio valido. Intente de nuevo.\n")
                continue

            localidad = municipio.seleccionar_localidad()
            if localidad == None:
                print("No se selecciono una localidad valida. Intente de nuevo.\n")
                continue

            if localidad.tiene_coordenadas() == True:
                return localidad
            else:
                print("La localidad seleccionada no tiene coordenadas registradas. Elija otra.\n")

    def validar_y_mostrar_estadisticas_consultas(self, consultas, estadisticas):
        """
        Muestra en pantalla el resumen de las consultas en tiempo real realizadas.
        """
        if len(consultas) == 0:
            print("Aun no has realizado ninguna consulta en tiempo real.")
            return

        print(f"Total de consultas realizadas hasta ahora: {len(consultas)}")

        for i, c in enumerate(consultas):
            print(f"{i + 1}. {c.localidad.nombre} ({c.localidad.municipio})- Temp {c.temperatura}°C")

        resumen = estadisticas.calcular_estadisticas(consultas)
        if resumen == None:
            print("Aun no has realizado alguna consulta.")
        else:
            print(
                f"Localidad mas calida: {resumen['mas_calida'].localidad.nombre} (Municipio {resumen['mas_calida'].localidad.municipio}): ({resumen['mas_calida'].temperatura}°C)\n"
                f"Localidad mas fria: {resumen['mas_fria'].localidad.nombre} (Municipio {resumen['mas_fria'].localidad.municipio}): ({resumen['mas_fria'].temperatura}°C)\n"
                f"Promedio de la consulta: {round(resumen['promedio'], 2)}°C"
            )