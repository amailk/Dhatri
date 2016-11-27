from flask import Flask, request, redirect

import twilio.twiml

app = Flask(__name__)

ASK_GREET = '''Hello! What would you like help with today? If you would like to ask a question, please press 1. If you would like to set an appointment with a midwife, please press 2. If you would like to change your registered information, please press 3. If you would like to speak with a representative, please press 4.”'''

@app.route("/welcome_ask", methods=["GET","POST"])
def welcome():

    r = twiml.Response()
    with.r.gather(action="/welcome_key" numDigits=1) as g:
        g.say(ASK_GREET)

    return str(r)

@app.route("/ask_key", methods=['GET', 'POST'])
def ask_key():
    digit_pressed = request.values.get('Digits', None)
    r = twiml.Response()

    if digit_pressed == "1":
        r.say("What would you like to ask?Press * at the end")
        #TODO: wit?
        r.say("“Please give me a minute while I look for the answer")
