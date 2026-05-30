import random
import pandas as pd

def generar_vacantes(cantidad):
    vacantes = []

    titulos = ["Odontólogo", "Desarrollador", "Diseñador", "Auxiliar", "Contador"]
    estados = ["activo", "cerrado"]

    for _ in range(cantidad):
        vacante = {
            "id": random.randint(1, 1000), # CORREGIDO: de ramdon a random
            "titulo": random.choice(titulos),
            "descripcion": "Descripción del cargo profesional",
            "salario": random.randint(1500000, 5000000),
            "estado": random.choice(estados)
        }
        vacantes.append(vacante)

    return vacantes

if __name__ == "__main__":
    # Generamos los datos (HU 3: Simulación)
    datos = generar_vacantes(20)
    df = pd.DataFrame(datos)

    # Exportamos en los dos formatos que pide la HU 3
    df.to_csv("vacantes.csv", index=False)
    df.to_json("vacantes.json", orient="records", indent=4)

    # Mostramos los primeros 5 registros (HU 2: head)
    print("--- Vista previa de las Vacantes (head) ---")
    print(df.head())

    print("\n--- Información técnica del DataFrame (info) ---")
    print(df.info())