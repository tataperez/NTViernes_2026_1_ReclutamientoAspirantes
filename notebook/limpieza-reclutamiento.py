from pathlib import Path

import pandas as pd


def limpiar_reclutamiento(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia y normaliza el DataFrame de reclutamiento (procesos de selección)."""
    df_limpio = df.copy()

    # Validar columnas requeridas
    columnas_requeridas = [
        "id",
        "cargo",
        "codigo",
        "estado",
        "salario_ofertado",
        "fecha_publicacion",
    ]
    faltantes = [col for col in columnas_requeridas if col not in df_limpio.columns]
    if faltantes:
        raise ValueError(f"Faltan columnas requeridas: {faltantes}")

    # Limpiar id: numérico y mayor a cero
    df_limpio["id"] = pd.to_numeric(df_limpio["id"], errors="coerce")
    df_limpio = df_limpio[df_limpio["id"] > 0]

    # Limpiar cargo: validar contra valores permitidos
    cargos_validos = [
        "desarrollador backend",
        "analista de datos",
        "diseñador ux",
    ]
    cargo_normalizado = (
        df_limpio["cargo"].astype("string").str.strip().str.lower()
    )
    df_limpio.loc[~cargo_normalizado.isin(cargos_validos), "cargo"] = pd.NA

    # Limpiar código: validar contra valores permitidos
    codigos_validos = ["rec001", "rec045", "rec300"]
    codigo_normalizado = (
        df_limpio["codigo"].astype("string").str.strip().str.lower()
    )
    df_limpio.loc[~codigo_normalizado.isin(codigos_validos), "codigo"] = pd.NA

    # Limpiar estado: validar contra valores permitidos
    estados_validos = ["activo", "en proceso", "finalizado"]
    estado_normalizado = (
        df_limpio["estado"].astype("string").str.strip().str.lower()
    )
    df_limpio.loc[~estado_normalizado.isin(estados_validos), "estado"] = pd.NA

    # Limpiar salario_ofertado: numérico con piso de validación
    df_limpio["salario_ofertado"] = pd.to_numeric(
        df_limpio["salario_ofertado"], errors="coerce"
    )
    df_limpio = df_limpio[df_limpio["salario_ofertado"] >= 1000000]

    # Limpiar fecha_publicacion: datetime válido
    df_limpio["fecha_publicacion"] = pd.to_datetime(
        df_limpio["fecha_publicacion"], errors="coerce"
    )
    fecha_default = pd.to_datetime("2026-01-01")
    df_limpio["fecha_publicacion"] = df_limpio["fecha_publicacion"].fillna(
        fecha_default
    )

    # Eliminar filas con columnas clave inválidas
    columnas_obligatorias = ["id", "cargo", "salario_ofertado", "codigo", "estado"]
    df_limpio = df_limpio.dropna(subset=columnas_obligatorias)

    return df_limpio.reset_index(drop=True)


if __name__ == "__main__":
    ruta_csv = Path("reclutamiento.csv")

    if not ruta_csv.exists():
        raise FileNotFoundError(
            "No se encontro reclutamiento.csv. Verifica la ruta del archivo."
        )

    df_original = pd.read_csv(ruta_csv)
    df_limpio = limpiar_reclutamiento(df_original)

    print("--- Vista previa de reclutamiento limpio (head) ---")
    print(df_limpio.head())
    print("\n--- Informacion tecnica del DataFrame limpio (info) ---")
    print(df_limpio.info())