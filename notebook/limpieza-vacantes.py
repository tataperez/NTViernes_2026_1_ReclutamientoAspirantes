from pathlib import Path

import pandas as pd


def limpiar_vacantes(vacantes) -> pd.DataFrame:
    """Limpia y estandariza datos de vacantes."""
    df = pd.DataFrame(vacantes).copy()

    columnas_requeridas = ["id", "titulo", "descripcion", "salario", "estado"]
    faltantes = [col for col in columnas_requeridas if col not in df.columns]
    if faltantes:
        raise ValueError(f"Faltan columnas requeridas: {faltantes}")

    # id numerico y mayor a cero
    df["id"] = pd.to_numeric(df["id"], errors="coerce")
    df = df[df["id"] > 0]

    # Normalizar titulo y validar catalogo permitido
    titulos_validos = ["odontologo", "desarrollador", "disenador", "auxiliar", "contador"]
    titulo_normalizado = (
        df["titulo"]
        .astype("string")
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
        .str.strip()
        .str.lower()
    )
    df["titulo"] = titulo_normalizado
    df.loc[~df["titulo"].isin(titulos_validos), "titulo"] = pd.NA

    # Normalizar descripcion
    df["descripcion"] = df["descripcion"].astype("string").str.strip()
    df.loc[df["descripcion"] == "", "descripcion"] = pd.NA

    # salario numerico con piso de validacion
    df["salario"] = pd.to_numeric(df["salario"], errors="coerce")
    df = df[df["salario"] >= 1000000]

    # estado en minuscula y validado
    estados_validos = ["activo", "cerrado"]
    df["estado"] = df["estado"].astype("string").str.strip().str.lower()
    df.loc[~df["estado"].isin(estados_validos), "estado"] = pd.NA

    # Columnas clave obligatorias para analisis
    df = df.dropna(subset=["id", "titulo", "salario", "estado"])

    return df.reset_index(drop=True)


if __name__ == "__main__":
    ruta_csv = Path("vacantes.csv")

    if not ruta_csv.exists():
        raise FileNotFoundError(
            "No se encontro vacantes.csv. Ejecuta primero la simulacion de vacantes."
        )

    df_sucio = pd.read_csv(ruta_csv)
    df_limpio = limpiar_vacantes(df_sucio)

    print("--- Vista previa de vacantes limpias (head) ---")
    print(df_limpio.head())
    print("\n--- Informacion tecnica del DataFrame limpio (info) ---")
    print(df_limpio.info())