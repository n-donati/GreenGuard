import requests

def recommendation1(total_invernaderos, salud_general, ultima_actualizacion):
    recommendation = requests.post("https://fridaplatform.com/generate", json={"inputs": f"Provea 2 pequeñas observaciones de un invernadero con las siguientes características a modo de párrafo: Total de invernaderos{total_invernaderos}, el porcentaje de los invernaderos con buena salud de este usuario es {salud_general}, y la última actualización de los datos fue hecha en {ultima_actualizacion}. Solo responda, no repita mi consulta.", "parameters": {"max_new_tokens": 150, "stream": True}})
    return recommendation.json()['generated_text']

# print(recommendation1(10, 90, "2022-01-01"))