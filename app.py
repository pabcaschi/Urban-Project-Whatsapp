from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/webhook", methods=['POST'])
def webhook():
    incoming_msg = request.form.get('Body')
    response = MessagingResponse()
    msg = response.message()

    if incoming_msg:
        # Aquí puedes personalizar la respuesta del bot
        msg.body(f"Hola, has dicho: {incoming_msg}")
    else:
        msg.body("No entendí tu mensaje.")

    return str(response)

if __name__ == "__main__":
import os

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
