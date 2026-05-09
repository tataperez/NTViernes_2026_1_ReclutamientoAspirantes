import pandas as pd

from notebook.descripcion import (
    describir_estructura,
    describir_estadisticas,
    describir_categoricas,
    describir_fechas,
    mostrar_muestras,
    inspeccionar_info,
    identificar_tipos,
    describir_calidad,
)
from notebook.limpieza import limpiar_datos
from utils.simulacion_reclutamiento import generar_simulacion

simulaciones = generar_simulacion(10)
print("Dataset cargado correctamente en DataFrame.")

simulaciones_ordenadas = pd.DataFrame(simulaciones)

simulaciones_limpias = limpiar_datos(simulaciones_ordenadas)
mostrar_muestras(simulaciones_limpias)
inspeccionar_info(simulaciones_limpias)
describir_estructura(simulaciones_limpias)
describir_estadisticas(simulaciones_limpias)
identificar_tipos(simulaciones_limpias)
describir_calidad(simulaciones_limpias)
describir_categoricas(simulaciones_limpias)
describir_fechas(simulaciones_limpias)
