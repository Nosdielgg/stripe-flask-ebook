import os
from flask import Flask, request, redirect, render_template
from dotenv import load_dotenv
import stripe
from utils.email_sender import send_ebook

load_dotenv()

app = Flask(__name__)

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

@app.route("/")
def index():
    return '''
    <form action="/create-checkout-session" method="POST">
        <button type="submit">Comprar e-book - R$ 9,99</button>
    </form>
    '''

@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "brl",
                    "product_data": {"name": "E-book Aprendizado Rápido"},
                    "unit_amount": 1990,
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url="https://seu-dominio.onrender.com/success",
            cancel_url="https://seu-dominio.onrender.com/cancel",
        )
        return redirect(session.url, code=303)
    except Exception as e:
        return str(e)

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/cancel")
def cancel():
    return "<h1>Compra cancelada.</h1>"

@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.data
    sig_header = request.headers.get("stripe-signature")
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except Exception:
        return "Webhook error", 400

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        email = session["customer_details"]["email"]
        send_ebook(email)

    return "OK", 200

if __name__ == "__main__":
    app.run(debug=True)
