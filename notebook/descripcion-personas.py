from __future__ import annotations

from pathlib import Path

import pandas as pd


def _to_python(value):
    """Convierte valores de pandas/numpy en tipos nativos."""
    if pd.isna(value):
        return None
    if hasattr(value, "item"):
        return value.item()
    return value


def descripcion_personas(df: pd.DataFrame) -> dict:
    """Genera un resumen descriptivo del DataFrame de personas."""
    total_filas, total_columnas = df.shape

    resumen = {
        "dimensiones": {
            "filas": int(total_filas),
            "columnas": int(total_columnas),
        },
        "tipos_dato": {col: str(tipo) for col, tipo in df.dtypes.items()},
        "nulos_por_columna": {col: int(n) for col, n in df.isna().sum().items()},
        "porcentaje_nulos_por_columna": {
            col: round((int(n) / total_filas) * 100, 2) if total_filas else 0.0
            for col, n in df.isna().sum().items()
        },
        "duplicados": {
            "filas_duplicadas": int(df.duplicated().sum()),
            "porcentaje": round((df.duplicated().sum() / total_filas) * 100, 2)
            if total_filas
            else 0.0,
        },
    }

    if "estado" in df.columns:
        estados = df["estado"].fillna("sin_dato").astype(str).str.strip().str.lower()
        distribucion = estados.value_counts(dropna=False)
        resumen["distribucion_estado"] = {k: int(v) for k, v in distribucion.items()}
        resumen["porcentaje_estado"] = {
            k: round((int(v) / total_filas) * 100, 2) if total_filas else 0.0
            for k, v in distribucion.items()
        }

    if "nombre" in df.columns:
        nombres = df["nombre"].fillna("sin_dato").astype(str).str.strip().str.lower()
        top_nombres = nombres.value_counts(dropna=False).head(10)
        resumen["top_nombres"] = {k: int(v) for k, v in top_nombres.items()}

    if "id" in df.columns:
        ids = pd.to_numeric(df["id"], errors="coerce")
        resumen["estadisticas_id"] = {
            "min": _to_python(ids.min()),
            "max": _to_python(ids.max()),
            "promedio": None if pd.isna(ids.mean()) else round(float(ids.mean()), 2),
            "mediana": _to_python(ids.median()),
            "valores_unicos": int(ids.nunique(dropna=True)),
        }

    if "fecha" in df.columns:
        fechas = pd.to_datetime(df["fecha"], errors="coerce", dayfirst=True)
        meses = fechas.dt.to_period("M").astype(str)
        conteo_mensual = meses.value_counts().sort_index()
        resumen["rango_fechas"] = {
            "min": None if pd.isna(fechas.min()) else str(fechas.min().date()),
            "max": None if pd.isna(fechas.max()) else str(fechas.max().date()),
        }
        resumen["personas_por_mes"] = {k: int(v) for k, v in conteo_mensual.items()}

    if "email" in df.columns:
        emails = df["email"].astype("string")
        dominio = emails.str.split("@").str[-1]
        top_dominios = dominio.value_counts(dropna=False).head(10)
        resumen["top_dominios_email"] = {k: int(v) for k, v in top_dominios.items()}

    return resumen


def imprimir_descripcion(resumen: dict) -> None:
    """Imprime el resumen de personas en formato legible."""
    print("=== DESCRIPCION GENERAL PERSONAS ===")
    print(
        f"Filas: {resumen['dimensiones']['filas']} | "
        f"Columnas: {resumen['dimensiones']['columnas']}"
    )

    print("\n=== TIPOS DE DATO ===")
    for columna, tipo in resumen["tipos_dato"].items():
        print(f"{columna}: {tipo}")

    print("\n=== CALIDAD DE DATOS ===")
    for columna, nulos in resumen["nulos_por_columna"].items():
        pct = resumen["porcentaje_nulos_por_columna"][columna]
        print(f"{columna}: {nulos} nulos ({pct}%)")
    print(
        "Filas duplicadas: "
        f"{resumen['duplicados']['filas_duplicadas']} "
        f"({resumen['duplicados']['porcentaje']}%)"
    )

    if "distribucion_estado" in resumen:
        print("\n=== DISTRIBUCION DE ESTADO ===")
        for estado, total in resumen["distribucion_estado"].items():
            pct = resumen["porcentaje_estado"][estado]
            print(f"{estado}: {total} ({pct}%)")

    if "top_nombres" in resumen:
        print("\n=== NOMBRES MAS FRECUENTES ===")
        for nombre, total in resumen["top_nombres"].items():
            print(f"{nombre}: {total}")

    if "estadisticas_id" in resumen:
        print("\n=== ESTADISTICAS ID ===")
        for clave, valor in resumen["estadisticas_id"].items():
            print(f"{clave}: {valor}")

    if "rango_fechas" in resumen:
        print("\n=== RANGO DE FECHAS ===")
        print(f"Min: {resumen['rango_fechas']['min']}")
        print(f"Max: {resumen['rango_fechas']['max']}")

    if "personas_por_mes" in resumen:
        print("\n=== PERSONAS POR MES ===")
        for mes, total in resumen["personas_por_mes"].items():
            print(f"{mes}: {total}")

    if "top_dominios_email" in resumen:
        print("\n=== DOMINIOS DE EMAIL MAS FRECUENTES ===")
        for dominio, total in resumen["top_dominios_email"].items():
            print(f"{dominio}: {total}")


if __name__ == "__main__":
    ruta_csv = Path("personas_generadas.csv")
    if not ruta_csv.exists():
        raise FileNotFoundError(
            "No se encontro personas_generadas.csv. Ejecuta primero la simulacion de personas."
        )

    datos = pd.read_csv(ruta_csv)
    resumen = descripcion_personas(datos)
    imprimir_descripcion(resumen)
