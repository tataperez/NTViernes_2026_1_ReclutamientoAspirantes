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


def descripcion_aspirantes(df: pd.DataFrame) -> dict:
    """Genera un resumen descriptivo del DataFrame de aspirantes."""
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

    if "nivel" in df.columns:
        niveles = df["nivel"].fillna("sin_dato").astype(str).str.strip().str.lower()
        distribucion = niveles.value_counts(dropna=False)
        resumen["distribucion_nivel"] = {k: int(v) for k, v in distribucion.items()}
        resumen["porcentaje_nivel"] = {
            k: round((int(v) / total_filas) * 100, 2) if total_filas else 0.0
            for k, v in distribucion.items()
        }

    if "experiencia_anos" in df.columns:
        experiencia = pd.to_numeric(df["experiencia_anos"], errors="coerce")
        resumen["estadisticas_experiencia"] = {
            "min": _to_python(experiencia.min()),
            "max": _to_python(experiencia.max()),
            "promedio": None
            if pd.isna(experiencia.mean())
            else round(float(experiencia.mean()), 2),
            "mediana": _to_python(experiencia.median()),
        }

    if "puntuacion" in df.columns:
        puntuaciones = pd.to_numeric(df["puntuacion"], errors="coerce")
        resumen["estadisticas_puntuacion"] = {
            "min": _to_python(puntuaciones.min()),
            "max": _to_python(puntuaciones.max()),
            "promedio": None
            if pd.isna(puntuaciones.mean())
            else round(float(puntuaciones.mean()), 2),
            "mediana": _to_python(puntuaciones.median()),
        }

    if "fecha_postulacion" in df.columns:
        fechas = pd.to_datetime(df["fecha_postulacion"], errors="coerce")
        meses = fechas.dt.to_period("M").astype(str)
        conteo_mensual = meses.value_counts().sort_index()
        resumen["rango_fechas"] = {
            "min": None if pd.isna(fechas.min()) else str(fechas.min().date()),
            "max": None if pd.isna(fechas.max()) else str(fechas.max().date()),
        }
        resumen["aspirantes_por_mes"] = {k: int(v) for k, v in conteo_mensual.items()}

    if "email" in df.columns:
        emails = df["email"].astype("string")
        dominio = emails.str.split("@").str[-1]
        top_dominios = dominio.value_counts(dropna=False).head(5)
        resumen["top_dominios_email"] = {k: int(v) for k, v in top_dominios.items()}

    if "id" in df.columns:
        ids = pd.to_numeric(df["id"], errors="coerce")
        resumen["estadisticas_id"] = {
            "min": _to_python(ids.min()),
            "max": _to_python(ids.max()),
            "valores_unicos": int(ids.nunique(dropna=True)),
        }

    return resumen


def imprimir_descripcion(resumen: dict) -> None:
    """Imprime el resumen de aspirantes en formato legible."""
    print("=== DESCRIPCION GENERAL ASPIRANTES ===")
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

    if "distribucion_nivel" in resumen:
        print("\n=== DISTRIBUCION DE NIVEL ===")
        for nivel, total in resumen["distribucion_nivel"].items():
            pct = resumen["porcentaje_nivel"][nivel]
            print(f"{nivel}: {total} ({pct}%)")

    if "estadisticas_experiencia" in resumen:
        print("\n=== ESTADISTICAS DE EXPERIENCIA (AÑOS) ===")
        for clave, valor in resumen["estadisticas_experiencia"].items():
            print(f"{clave}: {valor}")

    if "estadisticas_puntuacion" in resumen:
        print("\n=== ESTADISTICAS DE PUNTUACION ===")
        for clave, valor in resumen["estadisticas_puntuacion"].items():
            print(f"{clave}: {valor}")

    if "rango_fechas" in resumen:
        print("\n=== RANGO DE FECHAS DE POSTULACION ===")
        print(f"Min: {resumen['rango_fechas']['min']}")
        print(f"Max: {resumen['rango_fechas']['max']}")

    if "aspirantes_por_mes" in resumen:
        print("\n=== ASPIRANTES POR MES ===")
        for mes, total in resumen["aspirantes_por_mes"].items():
            print(f"{mes}: {total}")

    if "top_dominios_email" in resumen:
        print("\n=== TOP DOMINIOS DE EMAIL ===")
        for dominio, total in resumen["top_dominios_email"].items():
            print(f"{dominio}: {total}")

    if "estadisticas_id" in resumen:
        print("\n=== ESTADISTICAS ID ===")
        for clave, valor in resumen["estadisticas_id"].items():
            print(f"{clave}: {valor}")


if __name__ == "__main__":
    ruta_csv = Path("aspirantes.csv")
    if not ruta_csv.exists():
        raise FileNotFoundError(
            "No se encontro aspirantes.csv. Ejecuta primero la simulacion de aspirantes."
        )

    datos = pd.read_csv(ruta_csv)
    resumen = descripcion_aspirantes(datos)
    imprimir_descripcion(resumen)
