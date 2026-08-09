from SistemaMeteo import SistemaMeteo
from Municipio import Municipio
from Localidad import Localidad
from Clima_Actual import Clima_Actual
from RegistroHistorico import RegistroHistorico
from Validaciones import pedir_opcion_menu, pedir_fecha_valida
import estadisticas


# =====================================================================================
# Funcion principal de la aplicacion.
# Las validaciones de datos se gestionan externamente mediante el modulo Validaciones.py.
# Al solicitar opciones del menu o fechas, el sistema valida que las entradas sean correctas
# (numeros entre 1 y 5, o fechas con formato AAAA-MM-DD). Si el usuario ingresa letras,
# simbolos o valores fuera de rango, el programa muestra un mensaje de advertencia y solicita
# la opcion correcta sin detener su ejecucion.
# =====================================================================================
def ejecutar_app():
    try:
        sistema = SistemaMeteo("zonas_caracas.json")
    except Exception as e:
        print(f"Error al cargar el archivo de datos: {e}")
        return

    while True:
        print(
            "\n----Sistema Meteorologico de Caracas----\n"
            "1. Ver reporte inicial (Carga de datos)\n"
            "2. Consultar clima en tiempo real\n"
            "3. Consultar registro historico y datos\n"
            "4. Ver las estadisticas de la consulta\n"
            "5. Salir del programa"
        )

        opcion = pedir_opcion_menu("Seleccione la opcion de su preferencia: ", 1, 5)

        if opcion == 1:
            print("\n----Reporte inicial de cobertura----")
            sistema.reporte_inicial_total()

        elif opcion == 2:
            print("\n----Consulta en tiempo real----")
            municipio = sistema.seleccionar_municipio()
            if municipio:
                localidad = municipio.seleccionar_localidad()
                if localidad:
                    try:
                        clima = sistema.consultar_clima_actual(localidad)
                        if clima:
                            separador = "=" * 40
                            print(f"\n{separador}\n{clima}\n{separador}")
                    except Exception as e:
                        print(f"\nOcurrio un error al consultar el clima en tiempo real: {e}")

        elif opcion == 3:
            print("\n----Consulta de datos historicos----")
            municipio = sistema.seleccionar_municipio()
            if municipio:
                localidad = municipio.seleccionar_localidad()
                if localidad:
                    inicio = pedir_fecha_valida("Ingrese fecha de inicio (AAAA-MM-DD): ")
                    fin = pedir_fecha_valida("Ingrese fecha de fin (AAAA-MM-DD): ")

                    try:
                        historico = sistema.consultar_clima_historico(localidad, inicio, fin)
                        if historico:
                            separador = "=" * 40
                            promedio = estadisticas.calcular_promedio_temperatura(historico)
                            extremos = estadisticas.obtener_extremos_historicos(historico)

                            mensaje_extremos = ""
                            if extremos:
                                mensaje_extremos = (
                                    f"Anio mas caluroso: {extremos['caluroso'][0]} ({round(extremos['caluroso'][1], 1)}°C)\n"
                                    f"Anio mas fresco: {extremos['fresco'][0]} ({round(extremos['fresco'][1], 1)}°C)\n"
                                    f"Anio mas lluvioso: {extremos['lluvioso'][0]} ({round(extremos['lluvioso'][1], 1)}mm)\n"
                                    f"Anio mas humedo: {extremos['humedo'][0]} ({round(extremos['humedo'][1], 1)}%)\n"
                                )

                            print(
                                f"\n{separador}\n"
                                f"{historico}\n"
                                f"Temperatura promedio del periodo: {round(promedio, 2)}°C\n"
                                f"{mensaje_extremos}"
                                f"{separador}"
                            )

                            estadisticas.generar_grafica_historica(historico)
                    except Exception as e:
                        print(f"\nOcurrio un error al obtener la informacion historica: {e}")

        elif opcion == 4:
            print("\n----Ver estadisticas de la consulta----")
            if len(sistema.consultas) == 0:
                print("Aun no has realizado ninguna consulta en tiempo real.")
            else:
                print(f"Total de consultas realizadas hasta ahora: {len(sistema.consultas)}")

                for i, c in enumerate(sistema.consultas, 1):
                    print(f"{i}. {c.localidad.nombre} - Temp: {c.temperatura}°C")

                resumen = estadisticas.calcular_estadisticas(sistema.consultas)
                if resumen:
                    print(
                        f"\n--- Resumen General ---\n"
                        f"Localidad mas calida: {resumen['mas_calida'].localidad.nombre} ({resumen['mas_calida'].temperatura}°C)\n"
                        f"Localidad mas fria: {resumen['mas_fria'].localidad.nombre} ({resumen['mas_fria'].temperatura}°C)\n"
                        f"Promedio de la consulta: {round(resumen['promedio'], 2)}°C"
                    )

        elif opcion == 5:
            print("\nGracias por usar el sistema meteorologico de Caracas!")
            break