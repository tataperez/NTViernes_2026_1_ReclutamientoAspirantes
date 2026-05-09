import random
from datetime import datetime, timedelta
import pandas as pd


def generar_aspirantes(cantidad):
    """Genera datos simulados de aspirantes a procesos de reclutamiento."""
    aspirantes = []

    nombres = [
        "Juan Pérez",
        "María García",
        "Carlos López",
        "Ana Martínez",
        "Luis Rodríguez",
        "Sofía Fernández",
        "Pedro Sánchez",
        "Lucía Díaz",
        "Miguel Torres",
        "Isabel Ruiz",
    ]
    correos_dominios = [
        "gmail.com",
        "hotmail.com",
        "outlook.com",
        "yahoo.com",
        "example.com",
    ]
    niveles_experiencia = ["junior", "senior", "mid-level", "entry-level"]
    estados = ["en_revision", "aceptado", "rechazado", "entrevista", "oferta"]

    fecha_inicio = datetime.now() - timedelta(days=365)

    for i in range(cantidad):
        fecha_postulacion = fecha_inicio + timedelta(
            days=random.randint(0, 365)
        )
        nombre = random.choice(nombres)
        email_local = nombre.lower().replace(" ", ".") + str(random.randint(100, 999))

        aspirante = {
            "id": i + 1,
            "nombre": nombre,
            "email": f"{email_local}@{random.choice(correos_dominios)}",
            "telefono": f"+57{random.randint(3000000000, 3199999999)}",
            "experiencia_anos": random.randint(0, 20),
            "nivel": random.choice(niveles_experiencia),
            "fecha_postulacion": fecha_postulacion.strftime("%Y-%m-%d"),
            "estado": random.choice(estados),
            "puntuacion": random.randint(0, 100),
        }

        # Inyectar errores controlados para simular datos reales
        prob_error = random.random()
        if prob_error < 0.05:
            aspirante["experiencia_anos"] = None
        elif prob_error < 0.08:
            aspirante["email"] = None
        elif prob_error < 0.10:
            aspirante["telefono"] = "INVALIDO"
        elif prob_error < 0.12:
            aspirante["nivel"] = "DESCONOCIDO"
        elif prob_error < 0.15:
            aspirante["estado"] = "PENDIENTE_REVISAR"

        aspirantes.append(aspirante)

    return aspirantes


if __name__ == "__main__":
    # Generar 100 aspirantes
    datos = generar_aspirantes(100)

    # Convertir a DataFrame
    df = pd.DataFrame(datos)

    # Guardar en CSV
    df.to_csv("aspirantes.csv", index=False)

    # Mostrar vista previa
    print("--- Vista previa de aspirantes (head) ---")
    print(df.head())

    print("\n--- Información técnica del DataFrame ---")
    print(df.info())
