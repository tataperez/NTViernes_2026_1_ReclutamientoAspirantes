from pathlib import Path

import pandas as pd


def limpiar_aspirantes(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia y normaliza el DataFrame de aspirantes."""
    df_limpio = df.copy()

    # Validar columnas requeridas
    columnas_requeridas = [
        "id",
        "nombre",
        "email",
        "telefono",
        "experiencia_anos",
        "nivel",
        "fecha_postulacion",
        "estado",
        "puntuacion",
    ]
    faltantes = [col for col in columnas_requeridas if col not in df_limpio.columns]
    if faltantes:
        raise ValueError(f"Faltan columnas requeridas: {faltantes}")

    # Limpiar id: numérico y mayor a cero
    df_limpio["id"] = pd.to_numeric(df_limpio["id"], errors="coerce")
    df_limpio = df_limpio[df_limpio["id"] > 0]

    # Limpiar nombre: string sin espacios extras
    df_limpio["nombre"] = (
        df_limpio["nombre"].astype("string").str.strip().str.title()
    )
    df_limpio = df_limpio[df_limpio["nombre"].notna()]

    # Limpiar email: formato válido y minúsculas
    df_limpio["email"] = df_limpio["email"].astype("string").str.lower().str.strip()
    email_valido = df_limpio["email"].str.contains(r"^[\w\.-]+@[\w\.-]+\.\w+$", regex=True, na=False)
    df_limpio.loc[~email_valido, "email"] = pd.NA

    # Limpiar teléfono: solo dígitos y +
    df_limpio["telefono"] = df_limpio["telefono"].astype("string").str.strip()
    telefono_valido = df_limpio["telefono"].str.contains(r"^(\+\d{1,3})?\d{7,14}$", regex=True, na=False)
    df_limpio.loc[~telefono_valido, "telefono"] = pd.NA

    # Limpiar experiencia_anos: numérico entre 0 y 100
    df_limpio["experiencia_anos"] = pd.to_numeric(df_limpio["experiencia_anos"], errors="coerce")
    df_limpio.loc[(df_limpio["experiencia_anos"] < 0) | (df_limpio["experiencia_anos"] > 100), "experiencia_anos"] = pd.NA

    # Limpiar nivel: validar contra valores permitidos
    niveles_validos = ["junior", "mid-level", "senior", "entry-level"]
    nivel_normalizado = (
        df_limpio["nivel"]
        .astype("string")
        .str.strip()
        .str.lower()
    )
    df_limpio.loc[~nivel_normalizado.isin(niveles_validos), "nivel"] = pd.NA

    # Limpiar fecha_postulacion: datetime válido
    df_limpio["fecha_postulacion"] = pd.to_datetime(
        df_limpio["fecha_postulacion"], errors="coerce"
    )

    # Limpiar estado: validar contra valores permitidos
    estados_validos = ["en_revision", "aceptado", "rechazado", "entrevista", "oferta"]
    estado_normalizado = (
        df_limpio["estado"]
        .astype("string")
        .str.strip()
        .str.lower()
    )
    df_limpio.loc[~estado_normalizado.isin(estados_validos), "estado"] = pd.NA

    # Limpiar puntuacion: numérico entre 0 y 100
    df_limpio["puntuacion"] = pd.to_numeric(df_limpio["puntuacion"], errors="coerce")
    df_limpio.loc[(df_limpio["puntuacion"] < 0) | (df_limpio["puntuacion"] > 100), "puntuacion"] = pd.NA

    # Eliminar filas con columnas clave inválidas
    columnas_obligatorias = ["id", "nombre", "email", "nivel", "estado", "fecha_postulacion"]
    df_limpio = df_limpio.dropna(subset=columnas_obligatorias)

    return df_limpio.reset_index(drop=True)


if __name__ == "__main__":
    ruta_csv = Path("aspirantes.csv")

    if not ruta_csv.exists():
        raise FileNotFoundError(
            "No se encontro aspirantes.csv. Ejecuta primero la simulacion de aspirantes."
        )

    df_original = pd.read_csv(ruta_csv)
    df_limpio = limpiar_aspirantes(df_original)

    print("--- Vista previa de aspirantes limpios (head) ---")
    print(df_limpio.head())
    print("\n--- Informacion tecnica del DataFrame limpio (info) ---")
    print(df_limpio.info())
