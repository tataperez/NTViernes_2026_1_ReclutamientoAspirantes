import sys
from pathlib import Path

import pandas as pd

# ── Ruta raíz del proyecto ───────────────────────────────────────────────────
ROOT_DIR = Path(__file__).resolve().parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# ── Simulación ───────────────────────────────────────────────────────────────
from utils.simulacion_aspirantes import generar_aspirantes
from utils.simulacion_personas import generar_personas
from utils.simulacion_procesos import generar_procesos
from utils.simulacion_reclutamiento import generar_simulacion
from utils.simulacion_vacantes import generar_vacantes

# ── Limpieza ─────────────────────────────────────────────────────────────────
from notebook.limpieza_aspirantes import limpiar_aspirantes
from notebook.limpieza_personas import limpiar_personas
from notebook.limpieza_procesos import limpiar_procesos
from notebook.limpieza_reclutamiento import limpiar_reclutamiento
from notebook.limpieza_vacantes import limpiar_vacantes

# ── Transformación ───────────────────────────────────────────────────────────
from notebook.transformacion_aspirantes import transformar_aspirantes
from notebook.transformacion_procesos import transformar_procesos
from notebook.transformacion_reclutamiento import transformar_reclutamiento
from notebook.transformacion_vacantes import transformar_vacantes

# ── Descripción ──────────────────────────────────────────────────────────────
from notebook.descripcion_aspirantes import (
    descripcion_aspirantes,
    imprimir_descripcion as imprimir_descripcion_aspirantes,
)
from notebook.descripcion_personas import (
    descripcion_personas,
    imprimir_descripcion as imprimir_descripcion_personas,
)
from notebook.descripcion_procesos import (
    descripcion_procesos,
    imprimir_descripcion as imprimir_descripcion_procesos,
)
from notebook.descripcion_reclutamiento import (
    describir_categoricas,
    describir_estadisticas,
    describir_estructura,
    describir_fechas,
)
from notebook.descripcion_vacantes import (
    descripcion_vacantes,
    imprimir_descripcion as imprimir_descripcion_vacantes,
)

# ── Graficación ──────────────────────────────────────────────────────────────
from notebook.graficacion_aspirantes import graficar_resultados as graficar_aspirantes
from notebook.graficacion_procesos import graficar_resultados as graficar_procesos
from notebook.graficacion_reclutamiento import graficar_resultados as graficar_reclutamiento
from notebook.graficacion_vacantes import graficar_resultados as graficar_vacantes

# Carpeta donde se guardarán todas las gráficas
GRAFICAS_DIR = ROOT_DIR / "graficas"


# ════════════════════════════════════════════════════════════════════════════
# AUTENTICACIÓN
# ════════════════════════════════════════════════════════════════════════════

def registrar_usuario() -> dict[str, str]:
    print("\n=== REGISTRO DE USUARIO ===")
    usuario = input("Ingrese usuario: ").strip()
    clave = input("Ingrese clave: ").strip()

    if not usuario or not clave:
        print("Datos inválidos. Se asignan credenciales por defecto.")
        return {"usuario": "admin", "clave": "1234"}

    print("Usuario registrado correctamente.")
    return {"usuario": usuario, "clave": clave}


def login(credenciales: dict[str, str]) -> bool:
    print("\n=== INICIO DE SESIÓN ===")
    intentos = 0

    while intentos < 3:
        usuario = input("Usuario: ").strip()
        clave = input("Clave: ").strip()

        if usuario == credenciales["usuario"] and clave == credenciales["clave"]:
            print("Inicio de sesión exitoso.")
            return True

        intentos += 1
        print(f"Credenciales incorrectas. Intentos restantes: {3 - intentos}")

    print("Acceso denegado.")
    return False


# ════════════════════════════════════════════════════════════════════════════
# ETAPAS DEL PIPELINE
# ════════════════════════════════════════════════════════════════════════════

def simular_datos() -> None:
    print("\n===== SIMULACIÓN =====")

    df_procesos = pd.DataFrame(generar_procesos(80))
    df_procesos.to_csv(ROOT_DIR / "procesos.csv", index=False)
    print(f"  ✔ procesos.csv           ({len(df_procesos)} registros)")

    df_personas = pd.DataFrame(generar_personas(60))
    df_personas.to_csv(ROOT_DIR / "personas_generadas.csv", index=False)
    print(f"  ✔ personas_generadas.csv ({len(df_personas)} registros)")

    df_vacantes = pd.DataFrame(generar_vacantes(40))
    df_vacantes.to_csv(ROOT_DIR / "vacantes.csv", index=False)
    df_vacantes.to_json(ROOT_DIR / "vacantes.json", orient="records", indent=4)
    print(f"  ✔ vacantes.csv / .json   ({len(df_vacantes)} registros)")

    df_reclutamiento = pd.DataFrame(generar_simulacion(80))
    df_reclutamiento.to_csv(ROOT_DIR / "reclutamiento.csv", index=False)
    print(f"  ✔ reclutamiento.csv      ({len(df_reclutamiento)} registros)")

    df_aspirantes = pd.DataFrame(generar_aspirantes(100))
    df_aspirantes.to_csv(ROOT_DIR / "aspirantes.csv", index=False)
    print(f"  ✔ aspirantes.csv         ({len(df_aspirantes)} registros)")

    print("Simulación completada.")


def limpiar_datos() -> None:
    print("\n===== LIMPIEZA =====")

    procesos = pd.read_csv(ROOT_DIR / "procesos.csv")
    limpiar_procesos(procesos).to_csv(ROOT_DIR / "procesos_limpio.csv", index=False)
    print("  ✔ procesos_limpio.csv")

    personas = pd.read_csv(ROOT_DIR / "personas_generadas.csv")
    limpiar_personas(personas).to_csv(ROOT_DIR / "personas_limpio.csv", index=False)
    print("  ✔ personas_limpio.csv")

    vacantes = pd.read_csv(ROOT_DIR / "vacantes.csv")
    limpiar_vacantes(vacantes).to_csv(ROOT_DIR / "vacantes_limpio.csv", index=False)
    print("  ✔ vacantes_limpio.csv")

    reclutamiento = pd.read_csv(ROOT_DIR / "reclutamiento.csv")
    limpiar_reclutamiento(reclutamiento).to_csv(
        ROOT_DIR / "reclutamiento_limpio.csv", index=False
    )
    print("  ✔ reclutamiento_limpio.csv")

    aspirantes = pd.read_csv(ROOT_DIR / "aspirantes.csv")
    limpiar_aspirantes(aspirantes).to_csv(ROOT_DIR / "aspirantes_limpio.csv", index=False)
    print("  ✔ aspirantes_limpio.csv")

    print("Limpieza completada.")


def describir_datos() -> None:
    print("\n===== DESCRIPCIÓN =====")

    df_procesos = pd.read_csv(ROOT_DIR / "procesos_limpio.csv")
    resumen_procesos = descripcion_procesos(df_procesos)
    imprimir_descripcion_procesos(resumen_procesos)

    df_personas = pd.read_csv(ROOT_DIR / "personas_limpio.csv")
    resumen_personas = descripcion_personas(df_personas)
    imprimir_descripcion_personas(resumen_personas)

    df_vacantes = pd.read_csv(ROOT_DIR / "vacantes_limpio.csv")
    resumen_vacantes = descripcion_vacantes(df_vacantes)
    imprimir_descripcion_vacantes(resumen_vacantes)

    df_reclutamiento = pd.read_csv(ROOT_DIR / "reclutamiento_limpio.csv")
    print("\n=== DESCRIPCIÓN GENERAL RECLUTAMIENTO ===")
    describir_estructura(df_reclutamiento)
    describir_estadisticas(df_reclutamiento)
    describir_categoricas(df_reclutamiento)
    describir_fechas(df_reclutamiento)

    df_aspirantes = pd.read_csv(ROOT_DIR / "aspirantes_limpio.csv")
    resumen_aspirantes = descripcion_aspirantes(df_aspirantes)
    imprimir_descripcion_aspirantes(resumen_aspirantes)


def graficar_datos() -> None:
    """
    Llama a cada módulo de graficación con el dict de resultados que
    entregan sus propias funciones de transformación.
    Cada módulo genera 5 gráficas y las guarda en graficas/<tema>/.
    """
    print("\n===== GRAFICACIÓN =====")
    print(f"  Carpeta de salida: {GRAFICAS_DIR}")

    # ── Aspirantes (5 gráficas) ──────────────────────────────────────────────
    df_aspirantes = pd.read_csv(ROOT_DIR / "aspirantes_limpio.csv")
    resultados_aspirantes = transformar_aspirantes(df_aspirantes)
    # Redirigimos la ruta de salida sobreescribiendo la constante del módulo
    import notebook.graficacion_aspirantes as _mod_asp
    _mod_asp.RUTA_ASSETS = str(GRAFICAS_DIR / "aspirantes")
    graficar_aspirantes(resultados_aspirantes)
    print("  ✔ 5 gráficas de aspirantes  → graficas/aspirantes/")

    # ── Procesos (5 gráficas) ────────────────────────────────────────────────
    df_procesos = pd.read_csv(ROOT_DIR / "procesos_limpio.csv")
    resultados_procesos = transformar_procesos(df_procesos)
    import notebook.graficacion_procesos as _mod_proc
    _mod_proc.RUTA_ASSETS = str(GRAFICAS_DIR / "procesos")
    graficar_procesos(resultados_procesos)
    print("  ✔ 5 gráficas de procesos    → graficas/procesos/")

    # ── Reclutamiento (5 gráficas) ───────────────────────────────────────────
    df_reclutamiento = pd.read_csv(ROOT_DIR / "reclutamiento_limpio.csv")
    resultados_reclutamiento = transformar_reclutamiento(df_reclutamiento)
    import notebook.graficacion_reclutamiento as _mod_rec
    _mod_rec.RUTA_ASSETS = str(GRAFICAS_DIR / "reclutamiento")
    graficar_reclutamiento(resultados_reclutamiento)
    print("  ✔ 5 gráficas de reclutamiento → graficas/reclutamiento/")

    # ── Vacantes (5 gráficas) ────────────────────────────────────────────────
    df_vacantes = pd.read_csv(ROOT_DIR / "vacantes_limpio.csv")
    resultados_vacantes = transformar_vacantes(df_vacantes)
    import notebook.graficacion_vacantes as _mod_vac
    _mod_vac.RUTA_ASSETS = str(GRAFICAS_DIR / "vacantes")
    graficar_vacantes(resultados_vacantes)
    print("  ✔ 5 gráficas de vacantes    → graficas/vacantes/")

    print(f"\nTotal: 20 gráficas generadas en {GRAFICAS_DIR}")
    print("Graficación completada.")


def ejecutar_pipeline_completo() -> None:
    print("\n========== PIPELINE COMPLETO ==========")
    simular_datos()
    limpiar_datos()
    describir_datos()
    graficar_datos()
    print("\n========== PIPELINE FINALIZADO ==========")


# ════════════════════════════════════════════════════════════════════════════
# MENÚ
# ════════════════════════════════════════════════════════════════════════════

def mostrar_menu() -> None:
    print("\n----- MENÚ RECLUTAMIENTO -----")
    print("1. Simular datos")
    print("2. Limpiar datos")
    print("3. Describir datos")
    print("4. Graficar datos")
    print("5. Ejecutar pipeline completo")
    print("6. Salir")


def pedir_opcion() -> int:
    try:
        return int(input("Seleccione opción: ").strip())
    except ValueError:
        return -1


# ════════════════════════════════════════════════════════════════════════════
# PUNTO DE ENTRADA
# ════════════════════════════════════════════════════════════════════════════

def main() -> None:
    print("=== SISTEMA DE RECLUTAMIENTO ===")
    print(f"Raíz del proyecto: {ROOT_DIR}")

    credenciales = registrar_usuario()
    if not login(credenciales):
        return

    opcion = 0
    while opcion != 6:
        mostrar_menu()
        opcion = pedir_opcion()

        if opcion == 1:
            simular_datos()
        elif opcion == 2:
            limpiar_datos()
        elif opcion == 3:
            describir_datos()
        elif opcion == 4:
            graficar_datos()
        elif opcion == 5:
            ejecutar_pipeline_completo()
        elif opcion == 6:
            print("Saliendo del sistema.")
        else:
            print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    main()
