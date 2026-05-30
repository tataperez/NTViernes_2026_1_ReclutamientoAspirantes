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
    # 1. Aspirantes por estado — barra + torta
    # =====================================================
    df_estado = resultados["por_estado"]

    graficar_barras(
        df_estado,
        columna_categorias="estado",
        columna_valores="cantidad",
        titulo="Aspirantes por estado",
        color_barras="#2196F3",
        nombre_archivo="aspirantes_por_estado_barra.png",
        ruta_destino=RUTA_ASSETS,
    )

    graficar_torta(
        df_estado,
        columna_etiquetas="estado",
        columna_valores="cantidad",
        titulo="Distribución de aspirantes por estado",
        nombre_archivo="aspirantes_por_estado_torta.png",
        ruta_destino=RUTA_ASSETS,
    )

    # =====================================================
    # 2. Aspirantes por nivel de experiencia — barra + torta
    # =====================================================
    df_nivel = resultados["por_nivel"]

    graficar_barras(
        df_nivel,
        columna_categorias="nivel",
        columna_valores="cantidad",
        titulo="Aspirantes por nivel de experiencia",
        color_barras="#4CAF50",
        nombre_archivo="aspirantes_por_nivel_barra.png",
        ruta_destino=RUTA_ASSETS,
    )

    graficar_torta(
        df_nivel,
        columna_etiquetas="nivel",
        columna_valores="cantidad",
        titulo="Distribución de aspirantes por nivel",
        nombre_archivo="aspirantes_por_nivel_torta.png",
        ruta_destino=RUTA_ASSETS,
    )

    # =====================================================
    # 3. Aspirantes registrados por fecha de postulación — línea
    # =====================================================
    df_fecha = resultados["por_fecha"]

    graficar_lineas(
        df_fecha,
        columna_eje_x="fecha_postulacion",
        columna_eje_y="cantidad_aspirantes",
        titulo="Aspirantes registrados por fecha de postulación",
        color_linea="#9C27B0",
        nombre_archivo="aspirantes_por_fecha_linea.png",
        ruta_destino=RUTA_ASSETS,
    )

    # =====================================================
    # 4. Puntuación promedio por nivel — barra
    # =====================================================
    df_puntuacion = resultados["puntuacion_por_nivel"]

    graficar_barras(
        df_puntuacion,
        columna_categorias="nivel",
        columna_valores="puntuacion_promedio",
        titulo="Puntuación promedio por nivel",
        color_barras="#FF9800",
        nombre_archivo="aspirantes_puntuacion_por_nivel_barra.png",
        ruta_destino=RUTA_ASSETS,
    )

    # =====================================================
    # 5. Cantidad de aspirantes por nivel y estado — mapa de calor
    # =====================================================
    df_nivel_estado = resultados["nivel_por_estado"]

    graficar_mapa_calor(
        df_nivel_estado,
        columna_filas="nivel",
        columna_columnas="estado",
        columna_valores="cantidad",
        titulo="Aspirantes por nivel y estado",
        paleta_color="Blues",
        nombre_archivo="aspirantes_nivel_por_estado_calor.png",
        ruta_destino=RUTA_ASSETS,
    )


if __name__ == "__main__":
    from pathlib import Path

    import pandas as pd

    from transformacion_aspirantes import transformar_aspirantes

    ruta_csv = Path("aspirantes.csv")

    if not ruta_csv.exists():
        raise FileNotFoundError(
            "No se encontro aspirantes.csv. Ejecuta primero la simulacion de aspirantes."
        )

    df = pd.read_csv(ruta_csv)
    resultados = transformar_aspirantes(df)
    graficar_resultados(resultados)
