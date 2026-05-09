import pandas as pd


def mostrar_muestras(data_frame_limpio, n: int = 5):
    print("**** MUESTRAS DE DATOS ****")
    print("--- head() ---")
    print(data_frame_limpio.head(n))
    print("\n--- tail() ---")
    print(data_frame_limpio.tail(n))


def inspeccionar_info(data_frame_limpio):
    print("\n**** INFORMACION DEL DATAFRAME ****")
    data_frame_limpio.info()


def describir_estructura(data_frame_limpio):
    print("\n**** ESTRUCTURA GENERAL ****")
    print(f"numero de filas: {data_frame_limpio.shape[0]}")
    print(f"numero de columnas: {data_frame_limpio.shape[1]}")
    print(f"Columnas disponibles: {list(data_frame_limpio.columns)}")


def describir_estadisticas(data_frame_limpio):
    print("\n**** ESTADISTICAS DESCRIPTIVAS ****")
    print(data_frame_limpio.describe(include="all"))


def identificar_tipos(data_frame_limpio):
    print("\n**** TIPOS DE VARIABLES ****")
    columnas_numericas = list(data_frame_limpio.select_dtypes(include=["number"]).columns)
    columnas_categoricas = list(data_frame_limpio.select_dtypes(include=["object", "string", "category"]).columns)
    print(f"Columnas numericas: {columnas_numericas}")
    print(f"Columnas categoricas: {columnas_categoricas}")


def describir_calidad(data_frame_limpio):
    print("\n**** CALIDAD DE DATOS ****")
    faltantes = data_frame_limpio.isna().sum()
    porcentaje_faltantes = (faltantes / len(data_frame_limpio) * 100).round(2)
    informe_calidad = pd.DataFrame({"faltantes": faltantes, "% faltantes": porcentaje_faltantes})
    print(informe_calidad)


def describir_categoricas(data_frame_limpio):
    print("\n**** FRECUENCIAS DE CATEGORICAS ****")
    print("Cargos publicados:")
    print(data_frame_limpio["cargo"].value_counts(dropna=False))
    print("\nCodigos de vacante:")
    print(data_frame_limpio["codigo"].value_counts(dropna=False))
    print("\nEstado de las vacantes:")
    print(data_frame_limpio["estado"].value_counts(dropna=False))


def describir_fechas(data_frame_limpio):
    print("\n**** RANGOS DE FECHAS ****")
    print(f"fecha minima: {data_frame_limpio['fecha_publicacion'].min()}")
    print(f"fecha maxima: {data_frame_limpio['fecha_publicacion'].max()}")
