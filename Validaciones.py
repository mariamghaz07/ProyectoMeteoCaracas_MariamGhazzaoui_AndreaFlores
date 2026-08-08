from datetime import datetime

#Validacion para seleccion del menu
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

#Validacion de formato correcto de la fecga
def pedir_fecha_valida(mensaje):
    """Solicita una fecha por consola y valida que cumpla el formato AAAA-MM-DD."""
    while True:
        fecha_str = input(mensaje).strip()
        try:
            datetime.strptime(fecha_str, "%Y-%m-%d")
            return fecha_str
        except ValueError:
            print("Formato de fecha invalido. Debe usar el formato AAAA-MM-DD (ejemplo: 2024-01-15). Intente de nuevo.\n")