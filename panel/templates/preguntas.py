from flask import Flask, render_template
import requests

app = Flask(__name__)

def preguntas():
    url = "https://backend-final1.onrender.com/api-auth/api/preguntas/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        preguntas = response.json()
        return preguntas  # Devolver la respuesta JSON completa
    except requests.exceptions.RequestException as e:
        print("Error al cargar las preguntas:", e)
        return None

@app.route('/')
def index():
    preguntas = obtener_preguntas()
    if preguntas:
        preguntas_texto = [pregunta['texto_pregunta'] for pregunta in preguntas]
        return render_template('preguntas.html', preguntas=preguntas_texto)
    else:
        return "Error al cargar las preguntas"

if __name__ == '__main__':
    app.run(debug=True)