import pandas as pd
def limpiar_datos(procesos):
    df = pd.DataFrame(procesos)

    # Limpiar idProceso
    df['idProceso'] = pd.to_numeric(df['idProceso'], errors='coerce')

    # Limpiar fechaInicio
    df['fechaInicio'] = pd.to_datetime(df['fechaInicio'], errors='coerce')

    # Limpiar estado
    estados_validos = ["en_proceso", "finalizado", "rechazado", "aprobado"]
    df['estado'] = df['estado'].str.strip().str.lower()
    df.loc[~df['estado'].isin(estados_validos), 'estado'] = None

    # Limpiar observaciones
    df['observaciones'] = df['observaciones'].apply(lambda x: x if isinstance(x, str) and x.strip() != "" else None)

    return df