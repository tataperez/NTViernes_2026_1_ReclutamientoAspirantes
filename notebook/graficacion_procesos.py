# Se importa os para manejar rutas y crear carpetas
import os
# Se agrega la carpeta raiz del proyecto al path para importar utils
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.graficacion import (
    graficar_barras,
    graficar_lineas,
    graficar_torta,
)

# Ruta típica de la carpeta assets en un proyecto React con Vite
RUTA_ASSETS = os.path.join(
    os.path.dirname(__file__), "..", "..", "mi-app-react", "src", "assets", "graficos"
)


def graficar_resultados(resultados: dict) -> None:

    # =====================================================
    # 1. Procesos por estado — barra + torta
    # =====================================================
    df_estado = resultados["procesos_por_estado"]

    graficar_barras(
        df_estado,
        columna_categorias="estado",
        columna_valores="cantidad",
        titulo="Procesos por estado",
        color_barras="#2196F3",
        nombre_archivo="procesos_por_estado_barra.png",
        ruta_destino=RUTA_ASSETS,
    )

    graficar_torta(
        df_estado,
        columna_etiquetas="estado",
        columna_valores="cantidad",
        titulo="Distribución de procesos por estado",
        nombre_archivo="procesos_por_estado_torta.png",
        ruta_destino=RUTA_ASSETS,
    )

    # =====================================================
    # 2. Procesos por fecha — línea
    # =====================================================
    df_fecha = resultados["procesos_por_fecha"]

    graficar_lineas(
        df_fecha,
        columna_eje_x="fechaInicio",
        columna_eje_y="cantidad_procesos",
        titulo="Cantidad de procesos por fecha",
        color_linea="#2196F3",
        nombre_archivo="procesos_por_fecha_linea.png",
        ruta_destino=RUTA_ASSETS,
    )

    # =====================================================
    # 3. Procesos aprobados por fecha — línea
    # =====================================================
    df_aprobados = resultados["aprobados_por_fecha"]

    graficar_lineas(
        df_aprobados,
        columna_eje_x="fechaInicio",
        columna_eje_y="cantidad_aprobados",
        titulo="Procesos aprobados por fecha",
        color_linea="#4CAF50",
        nombre_archivo="aprobados_por_fecha_linea.png",
        ruta_destino=RUTA_ASSETS,
    )

    # =====================================================
    # 4. Procesos rechazados por fecha — línea
    # =====================================================
    df_rechazados = resultados["rechazados_por_fecha"]

    graficar_lineas(
        df_rechazados,
        columna_eje_x="fechaInicio",
        columna_eje_y="cantidad_rechazados",
        titulo="Procesos rechazados por fecha",
        color_linea="#E91E63",
        nombre_archivo="rechazados_por_fecha_linea.png",
        ruta_destino=RUTA_ASSETS,
    )

    # =====================================================
    # 5. Observaciones más frecuentes — barra
    # =====================================================
    df_obs = resultados["observaciones_frecuentes"]

    graficar_barras(
        df_obs,
        columna_categorias="observaciones",
        columna_valores="cantidad",
        titulo="Observaciones más frecuentes",
        color_barras="#FF9800",
        nombre_archivo="observaciones_frecuentes_barra.png",
        ruta_destino=RUTA_ASSETS,
    )


if __name__ == "__main__":
    from pathlib import Path

    import pandas as pd

    from transformacion_procesos import transformar_procesos

    ruta_csv = Path("procesos.csv")

    if not ruta_csv.exists():
        raise FileNotFoundError(
            "No se encontro procesos.csv. Verifica la ruta del archivo."
        )

    df = pd.read_csv(ruta_csv)
    resultados = transformar_procesos(df)
    graficar_resultados(resultados)
