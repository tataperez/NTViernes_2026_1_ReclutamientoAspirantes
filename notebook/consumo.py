import requests


BASE_URL = "http://localhost:8080/api"


def consumir_aspirantes():
    url = f"{BASE_URL}/aspirantes"
    respuesta = requests.get(url)
    respuesta.raise_for_status()
    datos = respuesta.json()
    return datos


def consumir_personas():
    url = f"{BASE_URL}/personas"
    respuesta = requests.get(url)
    respuesta.raise_for_status()
    datos = respuesta.json()
    return datos


def consumir_vacantes():
    url = f"{BASE_URL}/vacantes"
    respuesta = requests.get(url)
    respuesta.raise_for_status()
    datos = respuesta.json()
    return datos


def consumir_procesos():
    url = f"{BASE_URL}/procesos"
    respuesta = requests.get(url)
    respuesta.raise_for_status()
    datos = respuesta.json()
    return datos


def consumir_reclutamiento():
    url = f"{BASE_URL}/reclutamiento"
    respuesta = requests.get(url)
    respuesta.raise_for_status()
    datos = respuesta.json()
    return datos
