from datetime import datetime, date, timedelta


def pedir_opcion_menu(mensaje, min_val=1, max_val=5):
    """Solicita un numero entero y valida que este dentro del rango especificado."""
    while True:
        try:
            opcion = int(input(mensaje).strip())
            if min_val <= opcion <= max_val:
                return opcion
            print(f"\nOpcion invalida. Debe presionar un numero del {min_val} al {max_val}.")
        except ValueError:
            print(f"\nEntrada invalida. Por favor, ingrese un numero entero del {min_val} al {max_val}.")


def pedir_fecha_valida(mensaje):
    """Solicita una fecha, valida el formato AAAA-MM-DD, que exista y este en rango de la API."""
    limite_minimo = date(1940, 1, 1)
    limite_maximo = date.today() - timedelta(days=5)

    while True:
        fecha_str = input(mensaje).strip()
        try:
            fecha_dt = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            
            if limite_minimo <= fecha_dt <= limite_maximo:
                return fecha_str
            else:
                print(f"Nuestros registros llegan desde 1940-01-01 hasta 5 dias atras ({limite_maximo}). Intente de nuevo.\n")
        except ValueError:
            print("Formato o fecha invalida. Debe usar el formato AAAA-MM-DD con una fecha real (ej: 2024-01-15).\n")


def pedir_rango_fechas():
    """Garantiza el ingreso de fecha inicio y fin, verificando que inicio < fin."""
    while True:
        inicio = pedir_fecha_valida("Ingrese fecha de inicio (AAAA-MM-DD): ")
        fin = pedir_fecha_valida("Ingrese fecha de fin (AAAA-MM-DD): ")

        f_inicio = datetime.strptime(inicio, "%Y-%m-%d").date()
        f_fin = datetime.strptime(fin, "%Y-%m-%d").date()

        if f_inicio < f_fin:
            return inicio, fin
        else:
            print("La fecha de inicio debe ser estrictamente menor a la fecha de fin. Intente de nuevo.\n")

def pedir_seleccion_lista(lista, titulo="Seleccione una opcion: "):
    """
    Muestra una lista numerada de objetos o cadenas y le pide al usuario
    seleccionar uno mediante su indice numerico.
    """
    for i, item in enumerate(lista, 1):
        print(f"{i}- {item}")
    
    indice = pedir_opcion_menu(titulo, 1, len(lista))
    return lista[indice - 1]


def pedir_localidad_por_nombre(sistema):
    """

    Pide el nombre de una localidad (completo o una parte) y la busca.
    Repite la busqueda si el usuario se equivoca o si la localidad 
    no tiene coordenadas.

    Parametros:
    - sistema: El sistema principal donde estan guardadas las localidades.

    Retorna:
    - La localidad que eligio el usuario y que si tiene coordenadas.

    """
    print("----INICIANDO SISTEMA DE BUSQUEDA POR NOMBRE----")
    cond = pedir_opcion_menu("Presiona (1) para escribir el nombre COMPLETO o (2) para escribir una PARTE: ", 1, 2)

    while True:
        if cond == 1:
            loc = input("Ingresa el nombre COMPLETO de la localidad: ").strip()
            posibles = sistema.buscar_nombre(loc)
            coincidencias = [l for l in posibles if l.nombre.lower() == loc.lower()]

            if not coincidencias:
                print("No se encontro ninguna localidad con ese nombre exacto. Intente de nuevo.\n")
                continue
            
            localidad = coincidencias[0]

        else:  # cond == 2
            loc = input("Ingresa una parte del nombre de la localidad: ").strip()
            posibles = sistema.buscar_nombre(loc)

            if not posibles:
                print("No tenemos registros de localidades con ese nombre, intente de nuevo.\n")
                continue

            localidad = pedir_seleccion_lista(posibles, "Ingresa la localidad a consultar por su indice: ")

        # Validacion de coordenadas
        if localidad.tiene_coordenadas():
            return localidad
        else:
            print("La localidad seleccionada no posee coordenadas registradas. Elija otra.\n")

def pedir_localidad_por_municipio(sistema):
    """
    Muestra los municipios y localidades para que el usuario elija una.
    Verifica que la localidad elegida tenga coordenadas validas.

    Parametros:
    - sistema: El sistema principal donde estan los municipios y localidades.

    Retorna:
    - La localidad seleccionada que si cuenta con coordenadas.
    """
    while True:
        municipio = sistema.seleccionar_municipio()
        if not municipio:
            print("No se selecciono un municipio valido. Intente de nuevo.\n")
            continue
        
        localidad = municipio.seleccionar_localidad()
        if not localidad:
            print("No se selecciono una localidad valida. Intente de nuevo.\n")
            continue


        if localidad.tiene_coordenadas():
            return localidad
        else:
            print("La localidad seleccionada no tiene coordenadas registradas. Elija otra.\n")





def validar_y_mostrar_estadisticas_consultas(consultas, estadisticas):
    """
    Revisa si hay consultas en tiempo real realizadas para mostrar el ranking 
    y los promedios de temperatura.

    Parametros:
    - consultas: Lista con las consultas hechas por el usuario.
    - estadisticas: Objeto que calcula los promedios y temperaturas extremas.
    """
    if not consultas:
        print("Aun no has realizado ninguna consulta en tiempo real.")
        return

    print(f"Total de consultas realizadas hasta ahora: {len(consultas)}")

    for i, c in enumerate(consultas, 1):
        print(f"{i}. {c.localidad.nombre} ({c.localidad.municipio})- Temp {c.temperatura}")
    
    resumen = estadisticas.calcular_estadisticas(consultas)
    if not resumen:
        print("Aun no has realizado alguna consulta.")
    else:
        print(
            f"Localidad mas calida: {resumen['mas_calida'].localidad.nombre} (Municipio {resumen['mas_calida'].localidad.municipio}): ({resumen['mas_calida'].temperatura}°C)\n"
            f"Localidad mas fria: {resumen['mas_fria'].localidad.nombre} (Municipio {resumen['mas_fria'].localidad.municipio}): ({resumen['mas_fria'].temperatura}°C)\n"
            f"Promedio de la consulta: {round(resumen['promedio'], 2)}°C"
        )