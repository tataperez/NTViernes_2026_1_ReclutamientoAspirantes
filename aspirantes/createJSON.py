import json
from aspirantes import generarAspirantes, aspirante

generarAspirantes()

json_path = "c:/Users/tamay/OneDrive/Documents/CESDE/NTViernes_2026_1_ReclutamientoAspirantes/aspirantes/json/aspirantes.json"

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(aspirante, f, ensure_ascii=False, indent=4)

print("Archivo JSON generado exitosamente.")
