import pandas as pd
from pathlib import Path
import sys

PROYECTO_RAIZ = Path(__file__).resolve().parents[1]
if str(PROYECTO_RAIZ) not in sys.path:
    sys.path.insert(0, str(PROYECTO_RAIZ))

from utils.simulacion import generar_personas


def limpiar_datos(data_frame_sucio):
    data_frame_limpio = data_frame_sucio.copy()

    # Procesando textos del DataFrame sucio
    data_frame_limpio["nombre"] = data_frame_limpio["nombre"].astype("string").str.strip().str.lower()
    data_frame_limpio["email"] = data_frame_limpio["email"].astype("string").str.strip().str.lower()
    data_frame_limpio["telefono"] = data_frame_limpio["telefono"].astype("string").str.strip()

    # Validar nombre: solo letras y espacios intermedios
    data_frame_limpio["nombre"] = data_frame_limpio["nombre"].where(
        data_frame_limpio["nombre"].str.match(r"^[a-z]+(?: [a-z]+)*$", na=False),
        pd.NA,
    )

    # Validar formato de email
    data_frame_limpio["email"] = data_frame_limpio["email"].where(
        data_frame_limpio["email"].str.match(r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$", na=False),
        pd.NA,
    )

    # Validar telefono: solo digitos y longitud 10
    data_frame_limpio["telefono"] = data_frame_limpio["telefono"].where(
        data_frame_limpio["telefono"].str.match(r"^\d{10}$", na=False),
        pd.NA,
    )

    # Limpieza de datos numericos
    ids_numericos = pd.to_numeric(data_frame_limpio["id"], errors="coerce")
    ids_validos = ids_numericos.where((ids_numericos > 0) & (ids_numericos % 1 == 0))
    data_frame_limpio["id"] = ids_validos.astype("Int64")

    # Limpieza de fechas
    data_frame_limpio["fecha"] = pd.to_datetime(data_frame_limpio["fecha"], errors="coerce")
    fecha_default = pd.to_datetime("2026-01-01")
    data_frame_limpio["fecha"] = data_frame_limpio["fecha"].fillna(fecha_default)

    # Eliminar filas con campos obligatorios vacios
    columnas_obligatorias = ["id", "nombre", "email", "telefono"]
    data_frame_limpio = data_frame_limpio.dropna(subset=columnas_obligatorias)

    return data_frame_limpio


if __name__ == "__main__":
    personas_df = pd.DataFrame(generar_personas(1000))
    personas_limpias_ordenadas = limpiar_datos(personas_df).sort_values(by=["id", "nombre"])
    ruta_salida = Path(__file__).resolve().parent / "resultados_limpios_ordenados.csv"
    personas_limpias_ordenadas.to_csv(ruta_salida, index=False)

    print("DATOS LIMPIOS Y ORDENADOS")
    print(f"Registros sucios: {len(personas_df)}")
    print(f"Registros limpios: {len(personas_limpias_ordenadas)}")
    print(f"Archivo generado: {ruta_salida}")
    print(personas_limpias_ordenadas.head(20))