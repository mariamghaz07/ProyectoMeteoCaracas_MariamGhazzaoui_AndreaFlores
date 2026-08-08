
class Estadisticas:
    def __init__(self):
        pass

    def obtener_extremos_historicos(self, registro_historico):
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
        sumas_precip = {ano: sum(v) for ano, v in precip_por_ano.items()}
        prom_hum = {ano: sum(v) / len(v) for ano, v in hum_por_ano.items() if len(v) > 0}

        ano_mas_caluroso = max(prom_temp, key=prom_temp.get)
        ano_mas_fresco = min(prom_temp, key=prom_temp.get)
        ano_mas_lluvioso = max(sumas_precip, key=sumas_precip.get)
        ano_mas_humedo = max(prom_hum, key=prom_hum.get)

        return {"caluroso": (ano_mas_caluroso, prom_temp[ano_mas_caluroso]),"fresco": (ano_mas_fresco, prom_temp[ano_mas_fresco]), "lluvioso": (ano_mas_lluvioso, sumas_precip[ano_mas_lluvioso]), "humedo": (ano_mas_humedo, prom_hum[ano_mas_humedo])}


    def calcular_estadisticas(self, lista_consulta):
        if not lista_consulta:
            return None

        mas_calida = max(lista_consulta, key=lambda c: c.temperatura)
        mas_fria = min(lista_consulta, key=lambda c: c.temperatura)
        promedio_temp = sum(c.temperatura for c in lista_consulta) / len(lista_consulta)

        return { "mas_calida": mas_calida, "mas_fria": mas_fria, "promedio": promedio_temp}

    def mostrar_localidades_sin_coordenadas(self, lista_municipios):
        for municipio in lista_municipios:
            print("----------------------------")
            print(f"Municipio: {municipio.nombre}")
            print("----------------------------")
            for localidad in municipio.localidades: 
                if localidad.tiene_coordenadas() == False:
                    print(f"{localidad.nombre}")

                
    


