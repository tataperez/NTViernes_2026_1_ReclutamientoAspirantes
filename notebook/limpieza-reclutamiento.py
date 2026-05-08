import pandas as pd

def limpiar_datos(data_frame_sucio):
    data_frame_limpio = data_frame_sucio.copy()

    
    data_frame_limpio["cargo"] = data_frame_limpio["cargo"].astype("string").str.strip().str.lower()
    data_frame_limpio["codigo"] = data_frame_limpio["codigo"].astype("string").str.strip().str.lower()
    data_frame_limpio["estado"] = data_frame_limpio["estado"].astype("string").str.strip().str.lower()

    
    valores_esperados_cargo = ["desarrollador backend", "analista de datos", "diseñador ux"]
    data_frame_limpio["cargo"] = data_frame_limpio["cargo"].where(
        data_frame_limpio["cargo"].isin(valores_esperados_cargo),
        pd.NA
    )

    valores_esperados_codigo = ["rec001", "rec045", "rec300"]
    data_frame_limpio["codigo"] = data_frame_limpio["codigo"].where(
        data_frame_limpio["codigo"].isin(valores_esperados_codigo),
        pd.NA
    )

    valores_esperados_estado = ["activo", "en proceso", "finalizado"]
    data_frame_limpio["estado"] = data_frame_limpio["estado"].where(
        data_frame_limpio["estado"].isin(valores_esperados_estado),
        pd.NA
    )

  
    data_frame_limpio["id"] = pd.to_numeric(data_frame_limpio["id"], errors="coerce")
    data_frame_limpio["salario_ofertado"] = pd.to_numeric(data_frame_limpio["salario_ofertado"], errors="coerce")

    
    data_frame_limpio = data_frame_limpio[data_frame_limpio["id"] > 0]
    data_frame_limpio = data_frame_limpio[data_frame_limpio["salario_ofertado"] >= 1000000]

    
    
    data_frame_limpio["fecha_publicacion"] = pd.to_datetime(data_frame_limpio["fecha_publicacion"], errors="coerce")

    
    fecha_default = pd.to_datetime("2026-01-01")
    data_frame_limpio["fecha_publicacion"] = data_frame_limpio["fecha_publicacion"].fillna(fecha_default)

    
    columnas_obligatorias = ["id", "cargo", "salario_ofertado", "codigo", "estado"]
    data_frame_limpio = data_frame_limpio.dropna(subset=columnas_obligatorias)

    return data_frame_limpio