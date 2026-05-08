import pandas as pd


def describir_estructura(data_frame_limpio):
    print("**** Estructura general ****")
    print(f"numero de filas: {data_frame_limpio.shape[0]}")
    print(f"numero de columnas: {data_frame_limpio.shape[1]}")
    print(f"Columnas disponibles: {list(data_frame_limpio.columns)}")


def describir_estadisticas(data_frame_limpio):
    print("\n**** ESTADISTICAS ****")
    print(f"{data_frame_limpio[['id', 'salario_ofertado']].describe()}")


def describir_categoricas(data_frame_limpio):
    print("\n**** FRECUENCIAS DE CATEGORICAS ****")
    print("Cargos publicados:")
    print(f"{data_frame_limpio['cargo'].value_counts()}")
    print("\nCodigos de vacante:")
    print(f"{data_frame_limpio['codigo'].value_counts()}")
    print("\nEstado de las vacantes:")
    print(f"{data_frame_limpio['estado'].value_counts()}")


def describir_fechas(data_frame_limpio):
    print("\n**** RANGOS DE FECHAS ****")
    print(f"fecha minima: {data_frame_limpio['fecha_publicacion'].min()}")
    print(f"fecha maxima: {data_frame_limpio['fecha_publicacion'].max()}")
