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