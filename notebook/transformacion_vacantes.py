from pathlib import Path

import pandas as pd


def transformar_vacantes(data_frame_limpio):
    resultados = {}

    # =====================================================
    # FILTRO 1:
    # Cantidad de vacantes por estado
    # =====================================================
    filtro1 = data_frame_limpio.query("estado in ['activo', 'cerrado']")

    agrupado1 = filtro1.groupby("estado").size().reset_index(name="cantidad")
    total1 = agrupado1["cantidad"].sum()
    agrupado1["porcentaje"] = (agrupado1["cantidad"] / total1 * 100).round(2)

    resultados["por_estado"] = agrupado1

    # =====================================================
    # FILTRO 2:
    # Cantidad de vacantes por título
    # =====================================================
    agrupado2 = data_frame_limpio.groupby("titulo").agg(
        cantidad=("id", "count"),
        salario_promedio=("salario", "mean"),
        salario_min=("salario", "min"),
        salario_max=("salario", "max"),
    ).reset_index()
    total2 = agrupado2["cantidad"].sum()
    agrupado2["porcentaje"] = (agrupado2["cantidad"] / total2 * 100).round(2)
    agrupado2["salario_promedio"] = agrupado2["salario_promedio"].round(2)

    resultados["por_titulo"] = agrupado2

    # =====================================================
    # FILTRO 3:
    # Salario promedio por título
    # =====================================================
    agrupado3 = (
        data_frame_limpio
        .groupby("titulo")
        .agg(salario_promedio=("salario", "mean"))
        .reset_index()
    )
    agrupado3["salario_promedio"] = agrupado3["salario_promedio"].round(2)

    resultados["salario_por_titulo"] = agrupado3

    # =====================================================
    # FILTRO 4:
    # Vacantes activas por título
    # =====================================================
    filtro4 = data_frame_limpio.query("estado == 'activo'")

    agrupado4 = (
        filtro4
        .groupby("titulo")
        .size()
        .reset_index(name="cantidad_activas")
    )

    resultados["activas_por_titulo"] = agrupado4

    # =====================================================
    # FILTRO 5:
    # Cantidad de vacantes por título y estado (mapa de calor)
    # =====================================================
    agrupado5 = (
        data_frame_limpio
        .groupby(["titulo", "estado"])
        .size()
        .reset_index(name="cantidad")
    )

    resultados["titulo_por_estado"] = agrupado5

    return resultados


if __name__ == "__main__":
    ruta_csv = Path("vacantes.csv")

    if not ruta_csv.exists():
        raise FileNotFoundError(
            "No se encontro vacantes.csv. Ejecuta primero la simulacion de vacantes."
        )

    df = pd.read_csv(ruta_csv)
    resultado = transformar_vacantes(df)

    print("--- Vacantes por estado ---")
    print(resultado["por_estado"])
    print("\n--- Vacantes por titulo ---")
    print(resultado["por_titulo"])
    print("\n--- Salario por titulo ---")
    print(resultado["salario_por_titulo"])
    print("\n--- Activas por titulo ---")
    print(resultado["activas_por_titulo"])
    print("\n--- Titulo por estado ---")
    print(resultado["titulo_por_estado"])
