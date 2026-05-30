import random
from datetime import datetime, timedelta

def generar_simulacion(numeroSimulaciones):

    cargos = ["desarrollador backend", "analista de datos", "diseñador ux"]
    codigos = ["rec001", "rec045", "rec300"]
    salarios = [3500000, 5000000, 7000000]
    estados = ["activo", "en proceso", "finalizado"]
    fechaInicio = datetime(2026, 1, 2)

    simulaciones = []
    for _ in range(numeroSimulaciones):

        simulacion = {
            "id": random.randint(0, 200),
            "cargo": random.choice(cargos),
            "salario_ofertado": random.choice(salarios),
            "codigo": random.choice(codigos),
            "estado": random.choice(estados),
            "fecha_publicacion": fechaInicio + timedelta(days=random.randint(0, 60))
        }

        probabilidadError = random.random()
        if probabilidadError < 0.2:
            simulacion["id"] = None
        elif probabilidadError < 0.4:
            simulacion["cargo"] = random.choice(["gerente de compras", "contador publico"])
        elif probabilidadError < 0.5:
            simulacion["salario_ofertado"] = random.choice([0, -500000, None])
        elif probabilidadError < 0.7:
            simulacion["codigo"] = " " + simulacion["codigo"].upper()
        elif probabilidadError < 0.8:
            simulacion["estado"] = random.choice(["ACTIVO", "  en proceso  ", "FINALIZADO"])
        elif probabilidadError < 0.9:
            simulacion["fecha_publicacion"] = None

        simulaciones.append(simulacion)
    return simulaciones