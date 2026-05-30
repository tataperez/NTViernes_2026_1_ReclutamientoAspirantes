import random
from datetime import datetime, timedelta
import pandas as pd

def generar_personas(cantidad):
    personas = []

    listaNombres = ['Juan', 'María', 'Carlos', 'Ana', 'Luis', 'Sofía', 'Pedro', 'Lucía', 'Miguel', 'Isabel']
    listaCorreos = ['juan@example.com', 'maria@example.com', 'carlos@example.com', 'ana@example.com', 'luis@example.com', 'sofia@example.com', 'pedro@example.com', 'lucia@example.com', 'miguel@example.com', 'isabel@example.com']
    listaTelefonos = ['1234567890', '0987654321', '5555555555', '1111111111', '2222222222', '3333333333', '4444444444', '6666666666', '7777777777', '8888888888']
    
    fechaInicio = datetime.now() - timedelta(days=365)

    for _ in range(cantidad):

        fecha = fechaInicio + timedelta(days=random.randint(0, 365))
        fecha_actual = datetime.now()

        if (fecha_actual - fecha).days <= 180:
            estado = 'activo'
        else:
            estado = 'inactivo'

        persona = {
            'id': random.randint(1, 5000),
            'nombre': random.choice(listaNombres),
            'email': random.choice(listaCorreos),
            'telefono': random.choice(listaTelefonos),
            'estado': estado,
            'fecha': fecha.strftime('%d-%m-%Y')
        }

        personas.append(persona)

    return personas


if __name__ == "__main__":
    # Generar 50 personas
    data = generar_personas(50)

    # Convertir a DataFrame
    df = pd.DataFrame(data)

    # Guardar en CSV
    df.to_csv("personas_generadas.csv", index=False)

    print(df.head())