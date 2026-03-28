import csv
from aspirantes import generarAspirantes, aspirante

generarAspirantes()

with open("c:/Users/tamay/OneDrive/Documents/CESDE/NTViernes_2026_1_ReclutamientoAspirantes/aspirantes/cvs/aspirantes.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=aspirante[0].keys())
    writer.writeheader()
    writer.writerows(aspirante)

print("Archivo generado.")