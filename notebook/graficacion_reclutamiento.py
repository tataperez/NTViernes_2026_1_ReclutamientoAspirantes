# Se importa os para manejar rutas y crear carpetas
import os
# Se agrega la carpeta raiz del proyecto al path para importar utils
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.graficacion import (
    graficar_barras,
    graficar_lineas,
    graficar_mapa_calor,
    graficar_torta,
)

# Ruta típica de la carpeta assets en un proyecto React con Vite
RUTA_ASSETS = os.path.join(
    os.path.dirname(__file__), "..", "..", "mi-app-react", "src", "assets", "graficos"
)


def graficar_resultados(resultados: dict) -> None:

    # =====================================================
    # 1. Reclutamientos por estado — barra + torta
    # =====================================================
    df_estado = resultados["por_estado"]

    graficar_barras(
        df_estado,
        columna_categorias="estado",
        columna_valores="cantidad",
        titulo="Reclutamientos por estado",
        color_barras="#2196F3",
        nombre_archivo="reclutamiento_por_estado_barra.png",
        ruta_destino=RUTA_ASSETS,
    )

    graficar_torta(
        df_estado,
        columna_etiquetas="estado",
        columna_valores="cantidad",
        titulo="Distribución de reclutamientos por estado",
        nombre_archivo="reclutamiento_por_estado_torta.png",
        ruta_destino=RUTA_ASSETS,
    )

    # =====================================================
    # 2. Reclutamientos por cargo — barra + torta
    # =====================================================
    df_cargo = resultados["por_cargo"]

    graficar_barras(
        df_cargo,
        columna_categorias="cargo",
        columna_valores="cantidad",
        titulo="Reclutamientos por cargo",
        color_barras="#4CAF50",
        nombre_archivo="reclutamiento_por_cargo_barra.png",
        ruta_destino=RUTA_ASSETS,
    )

    graficar_torta(
        df_cargo,
        columna_etiquetas="cargo",
        columna_valores="cantidad",
        titulo="Distribución de reclutamientos por cargo",
        nombre_archivo="reclutamiento_por_cargo_torta.png",
        ruta_destino=RUTA_ASSETS,
    )

    # =====================================================
    # 3. Reclutamientos por fecha de publicación — línea
    # =====================================================
    df_fecha = resultados["por_fecha"]

    graficar_lineas(
        df_fecha,
        columna_eje_x="fecha_publicacion",
        columna_eje_y="cantidad_publicaciones",
        titulo="Reclutamientos publicados por fecha",
        color_linea="#9C27B0",
        nombre_archivo="reclutamiento_por_fecha_linea.png",
        ruta_destino=RUTA_ASSETS,
    )

    # =====================================================
    # 4. Reclutamientos por código de proceso — barra + torta
    # =====================================================
    df_codigo = resultados["por_codigo"]

    graficar_barras(
        df_codigo,
        columna_categorias="codigo",
        columna_valores="cantidad",
        titulo="Reclutamientos por código de proceso",
        color_barras="#FF9800",
        nombre_archivo="reclutamiento_por_codigo_barra.png",
        ruta_destino=RUTA_ASSETS,
    )

    graficar_torta(
        df_codigo,
        columna_etiquetas="codigo",
        columna_valores="cantidad",
        titulo="Distribución de reclutamientos por código",
        nombre_archivo="reclutamiento_por_codigo_torta.png",
        ruta_destino=RUTA_ASSETS,
    )

    # =====================================================
    # 5. Reclutamientos por cargo y estado — mapa de calor
    # =====================================================
    df_cargo_estado = resultados["cargo_por_estado"]

    graficar_mapa_calor(
        df_cargo_estado,
        columna_filas="cargo",
        columna_columnas="estado",
        columna_valores="cantidad",
        titulo="Reclutamientos por cargo y estado",
        paleta_color="Oranges",
        nombre_archivo="reclutamiento_cargo_por_estado_calor.png",
        ruta_destino=RUTA_ASSETS,
    )


if __name__ == "__main__":
    from pathlib import Path

    import pandas as pd

    from transformacion_reclutamiento import transformar_reclutamiento

    ruta_csv = Path("reclutamiento.csv")

    if not ruta_csv.exists():
        raise FileNotFoundError(
            "No se encontro reclutamiento.csv. Verifica la ruta del archivo."
        )

    df = pd.read_csv(ruta_csv)
    resultados = transformar_reclutamiento(df)
    graficar_resultados(resultados)
