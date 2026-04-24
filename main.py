import pandas as pd

from utils.simulacion import generar_personas

personas = generar_personas(1000)

personas_df = pd.DataFrame(personas)
personas_sucias_ordenadas = personas_df.sort_values(by=["id", "nombre"], na_position="last")

print("DATOS SUCIOS ORDENADOS")
print(f"Registros: {len(personas_sucias_ordenadas)}")
print(personas_sucias_ordenadas.head(20))
