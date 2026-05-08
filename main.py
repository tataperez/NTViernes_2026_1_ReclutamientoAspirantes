import pandas as pd


from notebook.descripcion import describir_estructura
from utils.simulacion_reclutamiento import generar_simulacion


from notebook.limpieza import limpiar_datos


from notebook.descripcion import describir_estructura, describir_estadisticas, describir_categoricas, describir_fechas


simulaciones = generar_simulacion(10)


simulaciones_ordenadas = pd.DataFrame(simulaciones)


simulaciones_limpias = limpiar_datos(simulaciones_ordenadas)
describir_estructura(simulaciones_limpias)
describir_estadisticas(simulaciones_limpias)
describir_categoricas(simulaciones_limpias)
describir_fechas(simulaciones_limpias)
