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


def descripcion_vacantes(df: pd.DataFrame) -> dict:
    """Genera un resumen descriptivo del DataFrame de vacantes."""
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

    if "titulo" in df.columns:
        titulos = df["titulo"].fillna("sin_dato").astype(str).str.strip().str.lower()
        top_titulos = titulos.value_counts(dropna=False).head(10)
        resumen["top_titulos"] = {k: int(v) for k, v in top_titulos.items()}

    if "salario" in df.columns:
        salarios = pd.to_numeric(df["salario"], errors="coerce")
        resumen["estadisticas_salario"] = {
            "min": _to_python(salarios.min()),
            "max": _to_python(salarios.max()),
            "promedio": None
            if pd.isna(salarios.mean())
            else round(float(salarios.mean()), 2),
            "mediana": _to_python(salarios.median()),
        }

    if "id" in df.columns:
        ids = pd.to_numeric(df["id"], errors="coerce")
        resumen["estadisticas_id"] = {
            "min": _to_python(ids.min()),
            "max": _to_python(ids.max()),
            "valores_unicos": int(ids.nunique(dropna=True)),
        }

    if "descripcion" in df.columns:
        descripciones = df["descripcion"].astype("string")
        longitudes = descripciones.str.len()
        resumen["descripcion_texto"] = {
            "con_texto": int(descripciones.notna().sum()),
            "sin_texto": int(descripciones.isna().sum()),
            "longitud_promedio": None
            if pd.isna(longitudes.mean())
            else round(float(longitudes.mean()), 2),
        }

    return resumen


def imprimir_descripcion(resumen: dict) -> None:
    """Imprime el resumen de vacantes en formato legible."""
    print("=== DESCRIPCION GENERAL VACANTES ===")
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

    if "top_titulos" in resumen:
        print("\n=== TITULOS MAS FRECUENTES ===")
        for titulo, total in resumen["top_titulos"].items():
            print(f"{titulo}: {total}")

    if "estadisticas_salario" in resumen:
        print("\n=== ESTADISTICAS DE SALARIO ===")
        for clave, valor in resumen["estadisticas_salario"].items():
            print(f"{clave}: {valor}")

    if "estadisticas_id" in resumen:
        print("\n=== ESTADISTICAS ID ===")
        for clave, valor in resumen["estadisticas_id"].items():
            print(f"{clave}: {valor}")

    if "descripcion_texto" in resumen:
        print("\n=== DESCRIPCION (TEXTO) ===")
        for clave, valor in resumen["descripcion_texto"].items():
            print(f"{clave}: {valor}")


if __name__ == "__main__":
    ruta_csv = Path("vacantes.csv")
    if not ruta_csv.exists():
        raise FileNotFoundError(
            "No se encontro vacantes.csv. Ejecuta primero la simulacion de vacantes."
        )

    datos = pd.read_csv(ruta_csv)
    resumen = descripcion_vacantes(datos)
    imprimir_descripcion(resumen)
