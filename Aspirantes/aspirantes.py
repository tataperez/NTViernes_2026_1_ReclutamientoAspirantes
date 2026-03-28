import random
from datetime import datetime, timedelta

CARGOS = [
    "Desarrollador Backend", "Desarrollador Frontend", "Analista de Datos",
    "Gerente de Proyectos", "Diseñador UX", "DevOps Engineer",
    "Analista de Seguridad", "Scrum Master", "QA Engineer", "Arquitecto de Software"
]

ESTADOS = ["En revisión", "Entrevista agendada", "Prueba técnica", "Rechazado", "Seleccionado"]

aspirantes = []

def generarAspirantes():
    for _ in range(1000):
        aspirante = {
            "documento": random.randint(10000000, 99999999),
            "cargoAplicado": random.choice(CARGOS),
            "experiencia": random.randint(1, 10),
            "estadoProceso": random.choice(ESTADOS),
            "fechaRegistro": (datetime(2023, 1, 1) + timedelta(days=random.randint(0, 730))).strftime("%Y-%m-%d")
        }
        aspirantes.append(aspirante)

generarAspirantes()