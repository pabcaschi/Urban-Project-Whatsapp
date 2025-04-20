from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").lower()
    resp = MessagingResponse()
    msg = resp.message()

    if "hola" in incoming_msg:
        msg.body("¡Hola! Soy tu asistente de Urban Project.")
    elif "precio" in incoming_msg:
        msg.body("Dime el nombre de la propiedad y te envío el precio.")
    else:
        msg.body("Lo siento, no entendí tu mensaje. ¿Puedes repetirlo?")

    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
