from __future__ import annotations

import pandas as pd


def _to_python(value):
	"""Convierte valores de pandas/numpy en tipos nativos para serializacion."""
	if pd.isna(value):
		return None
	if hasattr(value, "item"):
		return value.item()
	return value


def descripcion_procesos(df: pd.DataFrame) -> dict:
	"""Genera un resumen descriptivo del DataFrame de procesos de reclutamiento."""
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
		estados = df["estado"].fillna("SIN_DATO").astype(str).str.strip().str.lower()
		distribucion = estados.value_counts(dropna=False)
		resumen["distribucion_estado"] = {k: int(v) for k, v in distribucion.items()}
		resumen["porcentaje_estado"] = {
			k: round((int(v) / total_filas) * 100, 2) if total_filas else 0.0
			for k, v in distribucion.items()
		}

	if "fechaInicio" in df.columns:
		fechas = pd.to_datetime(df["fechaInicio"], errors="coerce")
		meses = fechas.dt.to_period("M").astype(str)
		conteo_mensual = meses.value_counts().sort_index()
		resumen["rango_fechas"] = {
			"min": None if pd.isna(fechas.min()) else str(fechas.min().date()),
			"max": None if pd.isna(fechas.max()) else str(fechas.max().date()),
		}
		resumen["procesos_por_mes"] = {k: int(v) for k, v in conteo_mensual.items()}

	if "idProceso" in df.columns:
		ids = pd.to_numeric(df["idProceso"], errors="coerce")
		resumen["estadisticas_idProceso"] = {
			"min": _to_python(ids.min()),
			"max": _to_python(ids.max()),
			"promedio": None if pd.isna(ids.mean()) else round(float(ids.mean()), 2),
			"mediana": _to_python(ids.median()),
			"valores_unicos": int(ids.nunique(dropna=True)),
		}

	if "observaciones" in df.columns:
		obs = df["observaciones"].astype("string")
		longitudes = obs.str.len()
		resumen["observaciones"] = {
			"con_texto": int(obs.notna().sum()),
			"sin_texto": int(obs.isna().sum()),
			"longitud_promedio": None
			if pd.isna(longitudes.mean())
			else round(float(longitudes.mean()), 2),
		}

	return resumen


def imprimir_descripcion(resumen: dict) -> None:
	"""Imprime el resumen descriptivo en un formato legible."""
	print("=== DESCRIPCION GENERAL ===")
	print(
		f"Filas: {resumen['dimensiones']['filas']} | "
		f"Columnas: {resumen['dimensiones']['columnas']}"
	)

	print("\n=== TIPOS DE DATO ===")
	for columna, tipo in resumen["tipos_dato"].items():
		print(f"{columna}: {tipo}")

	print("\n=== CALIDAD DE DATOS ===")
	for columna, nulos in resumen["nulos_por_columna"].items():
		porcentaje = resumen["porcentaje_nulos_por_columna"][columna]
		print(f"{columna}: {nulos} nulos ({porcentaje}%)")
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

	if "rango_fechas" in resumen:
		print("\n=== RANGO DE FECHAS ===")
		print(f"Min: {resumen['rango_fechas']['min']}")
		print(f"Max: {resumen['rango_fechas']['max']}")

	if "procesos_por_mes" in resumen:
		print("\n=== PROCESOS POR MES ===")
		for mes, total in resumen["procesos_por_mes"].items():
			print(f"{mes}: {total}")

	if "estadisticas_idProceso" in resumen:
		print("\n=== ESTADISTICAS idProceso ===")
		for clave, valor in resumen["estadisticas_idProceso"].items():
			print(f"{clave}: {valor}")

	if "observaciones" in resumen:
		print("\n=== OBSERVACIONES ===")
		for clave, valor in resumen["observaciones"].items():
			print(f"{clave}: {valor}")


if __name__ == "__main__":
	datos = pd.read_csv("procesos.csv")
	resumen = descripcion_procesos(datos)
	imprimir_descripcion(resumen)
