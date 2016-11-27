from flask import Flask, request, redirect
#from __future__ import with_statement
from twilio import twiml

app = Flask(__name__)

REGISTER_GREET = ''' "Hello, Welcome to Dharti! Please listen closely for the follwing options. If you are calling because you have a question, please press 1. If you would like to register for our service, please press 2. If you would like to learn more about our service, please press 3."'''

@app.route("/", methods=["GET", "POST"])
def welcome():

    r = twiml.Response()
    with r.gather(action="/welcome_key", numDigits=1) as g:
        g.say(REGISTER_GREET)

    return str(r)

@app.route("/welcome_key", methods=['GET','POST'])
def welcome_key():
    r = twiml.Response()

    if 'Digits' in request.values:
        choice = request.values['Digits']

        if choice == '2':
            r.say('You selected 2')
            r.say("What is your last name?")
            r.record(transcribe="true", transcribeCallback="/welcome_key", action="/firstname", finishOnKey="*")
            return str(r)

        elif choice == '1':
            r.say('You need support. We are here to help!')
            return str(r)
        elif choice == '3':
            r.say('Dharti is a service to get you connected with midwives to have a positive pregnancy')
        else:
            r.say("Sorry, I don't understand that choice.")

    with r.gather(numDigits=1, action="/lastname") as gather:
        gather.say("")

    r.redirect('/welcome_key')

    #return str(r)

@app.route("/firstname", methods=['GET', 'POST'])
def firstname():
    r = twiml.Response()

    r.say("What is your first name?")
    r.record(transcribe="true", transcribeCallback="/transcribe_firstname", action="/register_phone", finishOnKey="*")
    return str(r)

@app.route("/register_dob", methods=['GET','POST'])
def register_dob():
    r = twiml.Response()

    r.say("What is your date of birth? Please state in the order: year, month, and then date. Press the star key when you're done.")
    r.record(transcribe="true", transcribeCallback="/transcribe_dob", action="/register_phone", finishOnKey="*")
    return str(r)


@app.route("/register_phone", methods=['GET','POST'])
def register_phone():
    r = twiml.Response()

    r.say("What is your phone number? Press the star key when you're done.")
    r.record(transcribe="true", transcribeCallback="/transcribe_phone", action="/register_mc", finishOnKey="*")
    return str(r)


@app.route("/register_mc", methods=['GET','POST'])
def register_mc():
    r = twiml.Response()

    r.say("When was your last menstrual cycle? Please state in the order: year, month, and then date. Press the star key when you're done.")
    r.record(transcribe="true", transcribeCallback="/transcribe_mc", action="/register_secondary", finishOnKey="*")
    return str(r)


@app.route("/register_secondary", methods=['GET','POST'])
def register_secondary():
    r = twiml.Response()

    r.say("What is your secondary contact's phone number? Press the star key when you're done.")
    r.record(transcribe="true", transcribeCallback="/transcribe_secondary", action="/register_address", finishOnKey="*")
    return str(r)


@app.route("/register_address", methods=['GET','POST'])
def register_address():
    r = twiml.Response()

    r.say("What is your address? Press the star key when you're done.")
    r.record(transcribe="true", transcribeCallback="/transcribe_address", action="/register_done", finishOnKey="*")
    return str(r)


@app.route("/register_done", methods=['GET','POST'])
def register_done():
    r = twiml.Response()

    with r.gather(action="/register_confirm", numDigits=1) as g:
        g.say("Thank you")
        g.say("Please press 1 if information is correct, press 2 otherwise")

    return str(r)

@app.route("/register_confirm", methods=['GET', 'POST'])
def register_confirm():
    digit_pressed = request.values.get('Digits', None)

    r = twiml.Response()
    if digit_pressed == 1:
        r.say("Thank you. You will receive a text to confirm that you have successfully registered. Please let us know when you have any concerns. Goodbye")
        r.hangup()
        #TODO
        sendText()
    elif digit_pressed == 2:
        r.redirect("/welcome")

    return str(r)

if __name__ == "__main__":
    app.run(debug=True)
