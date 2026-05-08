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

        # Inyectando errores controlados
        probabilidadError = random.random()
        if probabilidadError < 0.2:
            proceso["idProceso"] = None
        elif probabilidadError < 0.4:
            proceso["estado"] = random.choice(["pendiente", "cancelado", "EN_CURSO"])
        elif probabilidadError < 0.5:
            proceso["observaciones"] = random.choice([None, "", 12345])
        elif probabilidadError < 0.8:
            proceso["estado"] = " " + proceso["estado"].upper()
        elif probabilidadError < 0.9:
            proceso["fechaInicio"] = None

        procesos.append(proceso)

    return procesos

