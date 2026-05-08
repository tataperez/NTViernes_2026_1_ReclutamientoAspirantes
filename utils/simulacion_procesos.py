import random
from datetime import datetime, timedelta
import pandas as pd

def generar_procesos(cantidad):
    procesos = []

    estados = ["en_proceso", "finalizado", "rechazado", "aprobado"]
    observaciones = [
        "Buen perfil",
        "Falta experiencia",
        "Aprobado para siguiente fase",
        "No cumple requisitos"
    ]

    fechaInicio = datetime(2023, 1, 1)

    for i in range(cantidad):
        fecha = fechaInicio + timedelta(days=random.randint(0, 365))

        proceso = {
            "idProceso": i + 1,
            "fechaInicio": fecha.strftime("%Y-%m-%d"),
            "estado": random.choice(estados),
            "observaciones": random.choice(observaciones)
        }

        procesos.append(proceso)

    return procesos


df = pd.DataFrame(generar_procesos(30))
df.to_csv("procesos.csv", index=False)

print(df.head())