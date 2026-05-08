from pathlib import Path

import pandas as pd


def limpiar_personas(df: pd.DataFrame) -> pd.DataFrame:
	"""Limpia y normaliza el DataFrame de personas."""
	df_limpio = df.copy()

	df_limpio["nombre"] = df_limpio["nombre"].astype("string").str.strip()
	df_limpio["email"] = df_limpio["email"].astype("string").str.lower().str.strip()
	df_limpio["email"] = df_limpio["email"].fillna("sin_email@example.com")

	df_limpio["id"] = pd.to_numeric(df_limpio["id"], errors="coerce")
	df_limpio = df_limpio[df_limpio["id"] > 0]

	df_limpio["telefono"] = df_limpio["telefono"].astype("string").str.strip()
	df_limpio.loc[df_limpio["telefono"] == "abc123", "telefono"] = pd.NA

	df_limpio["fecha"] = pd.to_datetime(df_limpio["fecha"], errors="coerce")
	df_limpio = df_limpio.dropna(subset=["fecha"])

	return df_limpio.reset_index(drop=True)


if __name__ == "__main__":
	ruta_csv = Path("personas_generadas.csv")

	if not ruta_csv.exists():
		raise FileNotFoundError(
			"No se encontro personas_generadas.csv. Ejecuta primero la simulacion de personas."
		)

	df_original = pd.read_csv(ruta_csv)
	df_limpio = limpiar_personas(df_original)

	print("--- Vista previa de personas limpias (head) ---")
	print(df_limpio.head())
	print("\n--- Informacion tecnica del DataFrame limpio (info) ---")
	print(df_limpio.info())