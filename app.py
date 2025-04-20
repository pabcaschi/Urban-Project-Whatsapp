from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

app = Flask(__name__)

# Clave de API de OpenAI desde variable de entorno
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    resp = MessagingResponse()
    msg = resp.message()

    try:
        # Llamada a ChatGPT con el mensaje del usuario
        respuesta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente experto en bienes raíces. Responde siempre de forma clara y amable."},
                {"role": "user", "content": incoming_msg}
            ],
            max_tokens=150,
            temperature=0.7,
        )
        reply = respuesta["choices"][0]["message"]["content"].strip()
        msg.body(reply)

    except Exception as e:
        msg.body("Lo siento, ha ocurrido un error al procesar tu mensaje.")

    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
