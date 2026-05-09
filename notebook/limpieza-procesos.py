from pathlib import Path

import pandas as pd


def limpiar_procesos(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia y normaliza el DataFrame de procesos."""
    df_limpio = df.copy()

    # Validar columnas requeridas
    columnas_requeridas = ["idProceso", "fechaInicio", "estado", "observaciones"]
    faltantes = [col for col in columnas_requeridas if col not in df_limpio.columns]
    if faltantes:
        raise ValueError(f"Faltan columnas requeridas: {faltantes}")

    # Limpiar idProceso: numérico y mayor a cero
    df_limpio["idProceso"] = pd.to_numeric(df_limpio["idProceso"], errors="coerce")
    df_limpio = df_limpio[df_limpio["idProceso"] > 0]

    # Limpiar fechaInicio: datetime válido
    df_limpio["fechaInicio"] = pd.to_datetime(
        df_limpio["fechaInicio"], errors="coerce"
    )

    # Limpiar estado: validar contra valores permitidos
    estados_validos = ["en_proceso", "finalizado", "rechazado", "aprobado"]
    df_limpio["estado"] = df_limpio["estado"].astype("string").str.strip().str.lower()
    df_limpio.loc[~df_limpio["estado"].isin(estados_validos), "estado"] = pd.NA

    # Limpiar observaciones: eliminar vacíos
    df_limpio["observaciones"] = df_limpio["observaciones"].astype("string").str.strip()
    df_limpio.loc[df_limpio["observaciones"] == "", "observaciones"] = pd.NA

    # Eliminar filas con columnas clave inválidas
    columnas_obligatorias = ["idProceso", "fechaInicio", "estado"]
    df_limpio = df_limpio.dropna(subset=columnas_obligatorias)

    return df_limpio.reset_index(drop=True)


if __name__ == "__main__":
    ruta_csv = Path("procesos.csv")

    if not ruta_csv.exists():
        raise FileNotFoundError(
            "No se encontro procesos.csv. Verifica la ruta del archivo."
        )

    df_original = pd.read_csv(ruta_csv)
    df_limpio = limpiar_procesos(df_original)

    print("--- Vista previa de procesos limpios (head) ---")
    print(df_limpio.head())
    print("\n--- Informacion tecnica del DataFrame limpio (info) ---")
    print(df_limpio.info())