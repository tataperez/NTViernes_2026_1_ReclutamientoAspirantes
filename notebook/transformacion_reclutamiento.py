from pathlib import Path

import pandas as pd


def transformar_reclutamiento(data_frame_limpio):
    resultados = {}

    # =====================================================
    # FILTRO 1:
    # Cantidad de reclutamientos por estado
    # =====================================================
    filtro1 = data_frame_limpio.query("estado in ['activo', 'en proceso', 'finalizado']")

    agrupado1 = filtro1.groupby("estado").size().reset_index(name="cantidad")
    total1 = agrupado1["cantidad"].sum()
    agrupado1["porcentaje"] = (agrupado1["cantidad"] / total1 * 100).round(2)

    resultados["por_estado"] = agrupado1

    # =====================================================
    # FILTRO 2:
    # Cantidad de reclutamientos por cargo
    # =====================================================
    agrupado2 = data_frame_limpio.groupby("cargo").agg(
        cantidad=("id", "count"),
        salario_promedio=("salario_ofertado", "mean"),
        salario_min=("salario_ofertado", "min"),
        salario_max=("salario_ofertado", "max"),
    ).reset_index()
    total2 = agrupado2["cantidad"].sum()
    agrupado2["porcentaje"] = (agrupado2["cantidad"] / total2 * 100).round(2)
    agrupado2["salario_promedio"] = agrupado2["salario_promedio"].round(2)

    resultados["por_cargo"] = agrupado2

    # =====================================================
    # FILTRO 3:
    # Reclutamientos por fecha de publicación
    # =====================================================
    agrupado3 = (
        data_frame_limpio
        .groupby("fecha_publicacion")
        .size()
        .reset_index(name="cantidad_publicaciones")
    )

    resultados["por_fecha"] = agrupado3

    # =====================================================
    # FILTRO 4:
    # Reclutamientos por código de proceso
    # =====================================================
    agrupado4 = (
        data_frame_limpio
        .groupby("codigo")
        .size()
        .reset_index(name="cantidad")
    )
    total4 = agrupado4["cantidad"].sum()
    agrupado4["porcentaje"] = (agrupado4["cantidad"] / total4 * 100).round(2)

    resultados["por_codigo"] = agrupado4

    # =====================================================
    # FILTRO 5:
    # Cantidad de reclutamientos por cargo y estado (mapa de calor)
    # =====================================================
    agrupado5 = (
        data_frame_limpio
        .groupby(["cargo", "estado"])
        .size()
        .reset_index(name="cantidad")
    )

    resultados["cargo_por_estado"] = agrupado5

    return resultados


if __name__ == "__main__":
    ruta_csv = Path("reclutamiento.csv")

    if not ruta_csv.exists():
        raise FileNotFoundError(
            "No se encontro reclutamiento.csv. Verifica la ruta del archivo."
        )

    df = pd.read_csv(ruta_csv)
    resultado = transformar_reclutamiento(df)

    print("--- Reclutamientos por estado ---")
    print(resultado["por_estado"])
    print("\n--- Reclutamientos por cargo ---")
    print(resultado["por_cargo"])
    print("\n--- Reclutamientos por fecha ---")
    print(resultado["por_fecha"])
    print("\n--- Reclutamientos por codigo ---")
    print(resultado["por_codigo"])
    print("\n--- Cargo por estado ---")
    print(resultado["cargo_por_estado"])
