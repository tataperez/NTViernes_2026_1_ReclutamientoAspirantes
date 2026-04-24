import random
from datetime import datetime, timedelta
from typing import Any, Dict, List


def generar_simulacion_personas(numero_simulaciones: int) -> List[Dict[str, Any]]:
    nombres = ["juan", "maria", "carlos", "ana", "luis", "sofia", "pedro", "lucia"]
    dominios = ["example.com", "mail.com", "correo.com"]
    fecha_inicio = datetime(2026, 1, 2)

    simulaciones: List[Dict[str, Any]] = []

    for i in range(1, numero_simulaciones + 1):
        nombre = random.choice(nombres)
        email = f"{nombre}{random.randint(1, 999)}@{random.choice(dominios)}"
        telefono = "".join(str(random.randint(0, 9)) for _ in range(10))

        simulacion = {
            "id": i,
            "nombre": nombre,
            "email": email,
            "telefono": telefono,
            "fecha": fecha_inicio + timedelta(days=random.randint(0, 60)),
        }

        # Inyectando errores controlados
        probabilidad_error = random.random()
        if probabilidad_error < 0.2:
            simulacion["id"] = None
        elif probabilidad_error < 0.4:
            simulacion["nombre"] = random.choice(["", "12345", None])
        elif probabilidad_error < 0.5:
            simulacion["email"] = random.choice(["correo-invalido", None, f" {email.upper()} "])
        elif probabilidad_error < 0.8:
            simulacion["telefono"] = random.choice(["abc123", None, "123"])
        elif probabilidad_error < 0.9:
            simulacion["fecha"] = None

        simulaciones.append(simulacion)

    return simulaciones


def generar_personas(cantidad: int) -> List[Dict[str, Any]]:
    return generar_simulacion_personas(cantidad)


if __name__ == "__main__":
    cantidad = 1000
    personas = generar_personas(cantidad)
    print("DATOS SUCIOS")
    print(f"Total: {len(personas)}")
    for persona in personas[:100]:
        print(persona)