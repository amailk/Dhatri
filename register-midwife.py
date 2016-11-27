from flask import Flask, request, redirect

from twilio import twiml

app = Flask(__name__)

REGISTER_MIDWIFE_GREET = ''' "Hello Welcome to the Midwife Registry" '''

@app.route("/", methods=["GET", "POST"])
def welcome():

    r = twiml.Response()
    with.r.gather(action="/welcome_name",  numDigits=1) as g:
        g.say(REGISTER_MIDWIFE_GREET)

    return str(r)

@app.route("/welcome_name", methods=['GET', 'POST'])
def welcome_name():
    r = twiml.Response()

    r.say("What is your name? Press the * key when you are done")
    r.record(transcribe="true", transcribeCallback="/transcribe_welcome_name", action="/first_workday", finishOnKey="*")
    return str(r)

@app.route("/first_workday", methods=['GET', 'POST'])
def first_workday():
    r = twiml.Response()

    r.say("What will be your first work day?")
    r.record(transcribe="true", transcribeCallback="/transcribe_first_workday", action="/last_workday", finishOnKey="*")
    return str(r)

@app.route("/last_workday", methods=['GET', 'POST'])
def last_workday():
    r = twiml.Response()

    r.say("What will be your last work day?")
    r.record(transcribe="true", transcribeCallback="/transcribe_last_workday", action="/first_workhour", finishOnKey="*")
    return str(r)

@app.route("/first_workhour", methods=['GET', 'POST'])
def first_workhour():
    r = twiml.Response()

    r.say("What will be your first work hour?")
    r.record(transcribe="true", transcribeCallback="/transcribe_first_workhour", action="/last_workhour", finishOnKey="*")
    return str(r)

@app.route("/last_workhour", methods=['GET', 'POST'])
def last_workhour():
    r = twiml.Response()

    r.say("What will be your last work hour?")
    r.record(transcribe="true", transcribeCallback="/transcribe_last_workhour", action="/register_done", finishOnKey="*")
    return str(r)

@app.route("/register_done", methods=['GET', 'POST'])
def register_done():
    r = twiml.Response()

    with.r.gather(action="/register_confirm", numDigits=1) as g:
        g.say("Thank you")
        g.say("Please press 1 if information is correct, press 2 otherwise")

    return str(r)

@app.route("/register_confirm", methods=['GET', 'POST'])
def register_confirm():
    digit_pressed = request.values.get('Digits', None)

    r = twiml.Response()
    if digit_pressed == 1:
        r.say("Thank you. You will receive a text to to confirm that you have successfully registered. Please let us know when you have any concerns. Goodbye")
        r.hangup()
        #TODO
        sendText()
    elif digit_pressed == 2:
        r.redirect("/welcome_midwife")
    return str(r)

if __name__ == "__main__":
    app.run(debug=True)
