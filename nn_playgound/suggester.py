# import requests

# # parametros primera recomendacion y segunda
# crop = "Cucumber"
# disease = "Bacterial Wilt"

# recommendation1 = requests.post("https://fridaplatform.com/generate", json={"inputs": f"Provea 2 pequeñas observaciones de la planta {crop} a cuál crece actualmente en un invernadero con el estado de la planta predominante: (English state just for reference, yet answer in Spanish){disease}", "parameters": {"max_new_tokens": 400, "stream": True}})


# print(recommendation1.json()['generated_text'])

# # parametros de la segunda recomendacion
# first_state = "Healthy Leaf"
# first_percentage = 60
# second_state = "Blight Leaf"
# second_percentage = 30
# third_state = "Dark Leaf"
# third_percentage = 10


# recommendation2 = requests.post("https://fridaplatform.com/generate", json={"inputs": f"Provea un calificación del 1 al 10 de en qué tan buen estado se encuentra un invernadero dado las siguientes estadísticas y estado de la planta: %{first_percentage} de la planta {crop} se encuentra como[utilizar nombre del estado en español para responder] {first_state}, %{second_percentage} se encuentra en la condición de {second_state}, y %{third_percentage} se encuentra en la condición de {third_state}. [Presente la respuesta como un único pequeño párrafo]", "parameters": {"max_new_tokens": 300, "stream": True}})

# print(recommendation2.json()['generated_text'])

# # curl -X POST -H "Content-Type: application/json" -d '{"inputs":"Help my friend write a python function for tensorflow model training", "parameters":{"max_new_tokens":300, "stream":true}}' https://fridaplatform.com/generate 

import requests

# parametros primera recomendacion y segunda

def recommendation1(total_invernaderos, salud_general, ultima_actualizacion):
    recommendation = requests.post("https://fridaplatform.com/generate", json={"inputs": f"Provea 2 pequeñas observaciones de un invernadero con las siguientes características a modo de párrafo: Total de invernaderos{total_invernaderos}, el porcentaje de los invernaderos con buena salud de este usuario es {salud_general}, y la última actualización de los datos fue hecha en {ultima_actualizacion}. Solo responda, no repita mi consulta.", "parameters": {"max_new_tokens": 150, "stream": True}})
    return recommendation.json()['generated_text']

print(recommendation1(10, 90, "2022-01-01"))