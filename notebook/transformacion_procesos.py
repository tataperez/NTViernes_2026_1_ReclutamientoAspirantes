from pathlib import Path

import pandas as pd


def transformar_procesos(data_frame_limpio):
    resultados = {}

    filtro1 = data_frame_limpio.query(
        "estado in ['en_proceso', 'finalizado', 'rechazado', 'aprobado']"
    )

    agrupado1 = filtro1.groupby("estado").size().reset_index(name="cantidad")
    total = agrupado1["cantidad"].sum()
    agrupado1["porcentaje"] = (agrupado1["cantidad"] / total * 100).round(2)

    resultados["procesos_por_estado"] = agrupado1

    agrupado2 = (
        data_frame_limpio
        .groupby("fechaInicio")
        .size()
        .reset_index(name="cantidad_procesos")
    )

    resultados["procesos_por_fecha"] = agrupado2


    filtro3 = data_frame_limpio.query("estado == 'aprobado'")

    agrupado3 = (
        filtro3
        .groupby("fechaInicio")
        .size()
        .reset_index(name="cantidad_aprobados")
    )

    resultados["aprobados_por_fecha"] = agrupado3

    filtro4 = data_frame_limpio.query("estado == 'rechazado'")

    agrupado4 = (
        filtro4
        .groupby("fechaInicio")
        .size()
        .reset_index(name="cantidad_rechazados")
    )

    resultados["rechazados_por_fecha"] = agrupado4

    agrupado5 = (
        data_frame_limpio
        .groupby("observaciones")
        .size()
        .reset_index(name="cantidad")
        .sort_values(by="cantidad", ascending=False)
    )

    resultados["observaciones_frecuentes"] = agrupado5

    return resultados


if __name__ == "__main__":
    ruta_csv = Path("procesos.csv")

    if not ruta_csv.exists():
        raise FileNotFoundError(
            "No se encontro procesos.csv. Verifica la ruta del archivo."
        )

    df = pd.read_csv(ruta_csv)
    resultados = transformar_procesos(df)

    for clave, df_resultado in resultados.items():
        print(f"\n--- {clave} ---")
        print(df_resultado)