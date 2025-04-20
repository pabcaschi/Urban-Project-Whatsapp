from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

app = Flask(__name__)

# Claves de entorno
openai.api_key = os.environ.get("OPENAI_API_KEY")
system_prompt = os.environ.get("GPT_SYSTEM_PROMPT", "Eres el asistente de Pablo Castellano, agente inmobiliario en Sevilla.")

# Clasifica el tipo de persona que escribe (internamente)
def clasificar_usuario(mensaje):
    prompt_clasificacion = """
Eres un clasificador inteligente de mensajes de WhatsApp. Tu tarea es analizar el siguiente mensaje y clasificarlo SOLO como una de estas categorías:

- COMPRADOR: si quiere comprar una casa o pregunta por una propiedad.
- VENDEDOR: si quiere vender una casa o habla de su vivienda.
- CANDIDATO: si pregunta cómo trabajar en el sector o en IAD.
- AGENTE: si ya es parte del equipo de Pablo.
- OTRO: si no puedes clasificarlo claramente.

Mensaje: "{}"

Devuelve solo una palabra: COMPRADOR, VENDEDOR, CANDIDATO, AGENTE o OTRO.
""".format(mensaje)

    respuesta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt_clasificacion}
        ],
        max_tokens=5,
        temperature=0
    )

    categoria = respuesta["choices"][0]["message"]["content"].strip().upper()
    return categoria

# Lógica principal del webhook
@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    resp = MessagingResponse()
    msg = resp.message()

    try:
        tipo = clasificar_usuario(incoming_msg)

        if tipo == "COMPRADOR":
            respuesta = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Este cliente es comprador. Mensaje: {incoming_msg}"}
                ],
                max_tokens=300
            )
        elif tipo == "VENDEDOR":
            respuesta = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Este cliente es vendedor. Mensaje: {incoming_msg}"}
                ],
                max_tokens=300
            )
        elif tipo == "CANDIDATO":
            respuesta = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Este usuario quiere trabajar en IAD. Mensaje: {incoming_msg}"}
                ],
                max_tokens=300
            )
        elif tipo == "AGENTE":
            respuesta = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Este es un agente del equipo de Pablo. Mensaje: {incoming_msg}"}
                ],
                max_tokens=300
            )
        else:
            respuesta = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"No estoy seguro de cómo clasificar este mensaje. Mensaje: {incoming_msg}"}
                ],
                max_tokens=300
            )

        final_reply = respuesta["choices"][0]["message"]["content"].strip()
        msg.body(final_reply)

    except Exception as e:
        msg.body("Lo siento, ha ocurrido un error al procesar tu mensaje.")

    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
