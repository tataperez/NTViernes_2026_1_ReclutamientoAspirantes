from pathlib import Path

import pandas as pd


def transformar_aspirantes(data_frame_limpio):
    resultados = {}

    # =====================================================
    # FILTRO 1:
    # Cantidad de aspirantes por estado
    # =====================================================
    filtro1 = data_frame_limpio.query(
        "estado in ['en_revision', 'aceptado', 'rechazado', 'entrevista', 'oferta']"
    )

    agrupado1 = filtro1.groupby("estado").agg(
        cantidad=("id", "count"),
        puntuacion_promedio=("puntuacion", "mean"),
    ).reset_index()
    total1 = agrupado1["cantidad"].sum()
    agrupado1["porcentaje"] = (agrupado1["cantidad"] / total1 * 100).round(2)
    agrupado1["puntuacion_promedio"] = agrupado1["puntuacion_promedio"].round(2)

    resultados["por_estado"] = agrupado1

    # =====================================================
    # FILTRO 2:
    # Cantidad de aspirantes por nivel de experiencia
    # =====================================================
    agrupado2 = data_frame_limpio.groupby("nivel").agg(
        cantidad=("id", "count"),
        experiencia_promedio=("experiencia_anos", "mean"),
    ).reset_index()
    total2 = agrupado2["cantidad"].sum()
    agrupado2["porcentaje"] = (agrupado2["cantidad"] / total2 * 100).round(2)
    agrupado2["experiencia_promedio"] = agrupado2["experiencia_promedio"].round(2)

    resultados["por_nivel"] = agrupado2

    # =====================================================
    # FILTRO 3:
    # Aspirantes registrados por fecha de postulación
    # =====================================================
    agrupado3 = (
        data_frame_limpio
        .groupby("fecha_postulacion")
        .size()
        .reset_index(name="cantidad_aspirantes")
    )

    resultados["por_fecha"] = agrupado3

    # =====================================================
    # FILTRO 4:
    # Puntuación promedio por nivel
    # =====================================================
    agrupado4 = (
        data_frame_limpio
        .groupby("nivel")
        .agg(puntuacion_promedio=("puntuacion", "mean"))
        .reset_index()
    )
    agrupado4["puntuacion_promedio"] = agrupado4["puntuacion_promedio"].round(2)

    resultados["puntuacion_por_nivel"] = agrupado4

    # =====================================================
    # FILTRO 5:
    # Cantidad de aspirantes por nivel y estado (mapa de calor)
    # =====================================================
    agrupado5 = (
        data_frame_limpio
        .groupby(["nivel", "estado"])
        .size()
        .reset_index(name="cantidad")
    )

    resultados["nivel_por_estado"] = agrupado5

    return resultados


if __name__ == "__main__":
    ruta_csv = Path("aspirantes.csv")

    if not ruta_csv.exists():
        raise FileNotFoundError(
            "No se encontro aspirantes.csv. Ejecuta primero la simulacion de aspirantes."
        )

    df = pd.read_csv(ruta_csv)
    resultado = transformar_aspirantes(df)

    print("--- Aspirantes por estado ---")
    print(resultado["por_estado"])
    print("\n--- Aspirantes por nivel ---")
    print(resultado["por_nivel"])
    print("\n--- Aspirantes por fecha ---")
    print(resultado["por_fecha"])
    print("\n--- Puntuacion por nivel ---")
    print(resultado["puntuacion_por_nivel"])
    print("\n--- Nivel por estado ---")
    print(resultado["nivel_por_estado"])
