# Se importa os para manejar rutas y crear carpetas
import os
# Se agrega la carpeta raiz del proyecto al path para importar utils
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.graficacion import (
    graficar_barras,
    graficar_mapa_calor,
    graficar_torta,
)

# Ruta típica de la carpeta assets en un proyecto React con Vite
RUTA_ASSETS = os.path.join(
    os.path.dirname(__file__), "..", "..", "mi-app-react", "src", "assets", "graficos"
)


def graficar_resultados(resultados: dict) -> None:

    # =====================================================
    # 1. Vacantes por estado — barra + torta
    # =====================================================
    df_estado = resultados["por_estado"]

    graficar_barras(
        df_estado,
        columna_categorias="estado",
        columna_valores="cantidad",
        titulo="Vacantes por estado",
        color_barras="#2196F3",
        nombre_archivo="vacantes_por_estado_barra.png",
        ruta_destino=RUTA_ASSETS,
    )

    graficar_torta(
        df_estado,
        columna_etiquetas="estado",
        columna_valores="cantidad",
        titulo="Distribución de vacantes por estado",
        nombre_archivo="vacantes_por_estado_torta.png",
        ruta_destino=RUTA_ASSETS,
    )

    # =====================================================
    # 2. Vacantes por título — barra + torta
    # =====================================================
    df_titulo = resultados["por_titulo"]

    graficar_barras(
        df_titulo,
        columna_categorias="titulo",
        columna_valores="cantidad",
        titulo="Vacantes por título",
        color_barras="#4CAF50",
        nombre_archivo="vacantes_por_titulo_barra.png",
        ruta_destino=RUTA_ASSETS,
    )

    graficar_torta(
        df_titulo,
        columna_etiquetas="titulo",
        columna_valores="cantidad",
        titulo="Distribución de vacantes por título",
        nombre_archivo="vacantes_por_titulo_torta.png",
        ruta_destino=RUTA_ASSETS,
    )

    # =====================================================
    # 3. Salario promedio por título — barra
    # =====================================================
    df_salario = resultados["salario_por_titulo"]

    graficar_barras(
        df_salario,
        columna_categorias="titulo",
        columna_valores="salario_promedio",
        titulo="Salario promedio por título de vacante",
        color_barras="#FF9800",
        nombre_archivo="vacantes_salario_por_titulo_barra.png",
        ruta_destino=RUTA_ASSETS,
    )

    # =====================================================
    # 4. Vacantes activas por título — barra
    # =====================================================
    df_activas = resultados["activas_por_titulo"]

    graficar_barras(
        df_activas,
        columna_categorias="titulo",
        columna_valores="cantidad_activas",
        titulo="Vacantes activas por título",
        color_barras="#E91E63",
        nombre_archivo="vacantes_activas_por_titulo_barra.png",
        ruta_destino=RUTA_ASSETS,
    )

    # =====================================================
    # 5. Vacantes por título y estado — mapa de calor
    # =====================================================
    df_titulo_estado = resultados["titulo_por_estado"]

    graficar_mapa_calor(
        df_titulo_estado,
        columna_filas="titulo",
        columna_columnas="estado",
        columna_valores="cantidad",
        titulo="Vacantes por título y estado",
        paleta_color="Greens",
        nombre_archivo="vacantes_titulo_por_estado_calor.png",
        ruta_destino=RUTA_ASSETS,
    )


if __name__ == "__main__":
    from pathlib import Path

    import pandas as pd

    from transformacion_vacantes import transformar_vacantes

    ruta_csv = Path("vacantes.csv")

    if not ruta_csv.exists():
        raise FileNotFoundError(
            "No se encontro vacantes.csv. Ejecuta primero la simulacion de vacantes."
        )

    df = pd.read_csv(ruta_csv)
    resultados = transformar_vacantes(df)
    graficar_resultados(resultados)
