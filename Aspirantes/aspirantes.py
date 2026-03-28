import random
import csv
from datetime import datetime, timedelta

CARGOS = [
    "Desarrollador Backend", "Desarrollador Frontend", "Analista de Datos",
    "Gerente de Proyectos", "Diseñador UX", "DevOps Engineer",
    "Analista de Seguridad", "Scrum Master", "QA Engineer", "Arquitecto de Software"
]

ESTADOS = ["En revisión", "Entrevista agendada", "Prueba técnica", "Rechazado", "Seleccionado"]

aspirante = []

def generarAspirantes():
    for _ in range(1000):
        nuevo_aspirante = {
            "documento": random.randint(10000000, 99999999),
            "cargoAplicado": random.choice(CARGOS),
            "experiencia": random.randint(1, 10),
            "estadoProceso": random.choice(ESTADOS),
            "fechaRegistro": (datetime(2023, 1, 1) + timedelta(days=random.randint(0, 730))).strftime("%Y-%m-%d")
        }
        aspirante.append(nuevo_aspirante)

if __name__ == "__main__":
    generarAspirantes()

    with open("c:/Users/tamay/OneDrive/Documents/CESDE/NTViernes_2026_1_ReclutamientoAspirantes/aspirantes/cvs/aspirantes.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=aspirante[0].keys())
        writer.writeheader()
        writer.writerows(aspirante)

    print("Total: " + str(len(aspirante)) + " aspirantes generados.")
    print("Archivo aspirantes.csv generado.")