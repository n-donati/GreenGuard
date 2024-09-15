import requests

def recommendation1(total_invernaderos, salud_general, ultima_actualizacion):
    recommendation = requests.post("https://fridaplatform.com/generate", json={"inputs": f"Provea pequeñas observaciones, EN MENOS DE 150 PALABRAS, sobre un conjunto de invernaderos con las siguientes características a modo de párrafo: Total de invernaderos{total_invernaderos}, el porcentaje de los invernaderos con buena salud de este usuario es {salud_general}, y la última actualización de los datos fue hecha en {ultima_actualizacion}.", "parameters": {"max_new_tokens": 200, "stream": True}})
    return recommendation.json()['generated_text']

# print(recommendation1(10, 90, "2022-01-01"))