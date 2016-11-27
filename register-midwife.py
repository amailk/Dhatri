fom flask import Flask, request, redirect

from twilio import twiml

app = Flask(__name__)

REGISTER_MIDWIFE_GREET = ''' "Hello. Welcome to the Midwife Registry" '''

@app.route("/welcome_register", methods=["GET", "POST"])
def welcome():

    r = twiml.Response()
    with.r.gather(action="/welcome_key",  numDigits=1) as g:
        g.say(REGISTER_MIDWIFE_GREET)

    return str(r)
