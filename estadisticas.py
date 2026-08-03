import matplotlib.pyplot as plt



def calcular_promedio_temperatura(registro_historico):
    if not registro_historico.temperaturas:
        return 0.0
    return sum(registro_historico.temperaturas) / len(registro_historico.temperaturas)

def obtener_extremos_historicos(registro_historico):
    if not registro_historico.fechas:
        return None

    temp_por_ano = {}
    precip_por_ano = {}
    hum_por_ano = {}

    for i in range(len(registro_historico.fechas)):
        ano = registro_historico.fechas[i].split("-")[0]

        if ano not in temp_por_ano:
            temp_por_ano[ano] = []
            precip_por_ano[ano] = []
            hum_por_ano[ano] = []

        temp_por_ano[ano].append(registro_historico.temperaturas[i])
        precip_por_ano[ano].append(registro_historico.precipitaciones[i])
        hum_por_ano[ano].append(registro_historico.humedades[i])

    prom_temp = {ano: sum(v) / len(v) for ano, v in temp_por_ano.items() if len(v) > 0}
    sumas_precip = {ano: sum(v) / len(v) for ano, v in precip_por_ano.items()}
    prom_hum = {ano: sum(v) / len(v) for ano, v in hum_por_ano.items() if len(v) > 0}

    ano_mas_caluroso = max(prom_temp, key=prom_temp.get)
    ano_mas_fresco = min(prom_temp, key=prom_temp.get)
    ano_mas_lluvioso = max(sumas_precip, key=sumas_precip.get)
    ano_mas_humedo = max(prom_hum, key=prom_hum.get)

    return {"caluroso": (ano_mas_caluroso, prom_temp[ano_mas_caluroso]),"fresco": (ano_mas_fresco, prom_temp[ano_mas_fresco]), "lluvioso": (ano_mas_lluvioso, sumas_precip[ano_mas_lluvioso]), "humedo": (ano_mas_humedo, prom_hum[ano_mas_humedo])}

def generar_grafica_historica(registro_historico):
    x = registro_historico.fechas
    y = registro_historico.temperaturas

    plt.plot(x, y, color="blue", marker="o")

    plt.title(f"Evolucion del Clima - {registro_historico.localidad.nombre}")

    plt.xlabel("Fechas")

    plt.ylabel("Temperatura")

    plt.show()

def calcular_estadisticas(lista_consulta):
    if not lista_consulta:
        return None

    mas_calida = max(lista_consulta, key=lambda c: c.temperatura)
    mas_fria = min(lista_consulta, key=lambda c: c.temperatura)
    promedio_temp = sum(c.temperatura for c in lista_consulta / len(lista_consulta))

    return { "mas calido": mas_calida, "mas frio": mas_fria, "promedio": promedio_temp}



