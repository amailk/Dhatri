# API
#import pdb
#import mysql.connector

from flask import Flask, request, redirect
from twilio import TwilioRestException
from twilio.rest import TwilioRestClient 
from twilio import twiml
 
app = Flask(__name__)
# connecting to database
connection = mysql.connector.connect(user='user', password='dhatri', host='127.0.0.1', database='dhatri') 
cursor = connection.cursor()

addPersonalInfo = ("INSERT INTO personal_information "
			"(LastName, FirstName, Address, PhoneNumber, EmergencyNumber, LastMenstrualCycle, DateOfBirth) ""
			"VALUES (%(last)s, %(first)s, %(addr)s, %(phone)s, %(emergency)s, %(lastPeriod), %(dob)s")
			
addMidwifeInfo = ("INSERT INTO midwif_information "
			"(LastName, FirstName, FirstWorkDay, LastWorkDay, FirstWorkHour, LastWorkHour) "
			"VALUES (%(last)s, %(first)s, %(firstDay)s, %(LastDay)s, %(FirstHour)s, %(lastHour)")
			
addAppointment = ("INSERT INTO appointments "
			"(PatientFirstName, PatientLastName, PatientPhoneNumber, MidwifeFirstName, MidwifeLastName, MidwifePhoneNumber, Address, DateAndTime) "
			"VALUES (%(patFirst)s, %(patLast)s, %(patPhone)s, %(midFirst)s, %(midLast)s, %(midPhone), %(addr)s, %(dateAndTime)s")

# put your own credentials here 
ACCOUNT_SID = "AC255fb7bce73bceb6793a4f11b23d7419" 
AUTH_TOKEN = "b7b8e53c05aee4c8429f3644800c8b5e" 
 
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
 
try:
	message = client.messages.create(
		to="+19059660696", 
		from_="+12264002125", 
		body="Test SMS"
	) 
except TwilioRestException as e:
    print(e)
	
print(message.sid)

last = ""
first = ""
addr = ""
phone = ""
emergency = ""
lastPeriod = ""
dob = ""

# User Registration
GREETING = ''' "Hello. Please listen closely for the options. If you are calling because you have a question, please press 1. If you would like to register for our service, please press 2. If you would like to learn more about our service, please press 3.'''

@app.route("/welcome", methods=["GET", "POST"])
def welcome():

    r = twiml.Response()
    with r.gather(action="/welcome_key", numDigits=1) as g:
        g.say(GREETING)

    return str(r)

@app.route("/welcome_key", methods=['GET','POST'])
def welcome_key():
    digit_pressed = request.values.get('Digits', None)
    r = twiml.Response()

    if digit_pressed == "2":
        r.say("What is your name? Press the star key when you're done.")
        r.record(transcribe="true", transcribeCallback="/transcribe_name", action="/register_dob", finishOnKey="*")
        return str(r)
    elif digit_pressed == "1":
        r.say("What is your question")
        r.hangup()
        return str(r)
    elif digit_pressed == "3":
        r.say("More details about our service... blah blah")
        r.hangup()
        return str(r)


@app.route("/register_dob", methods=['GET','POST'])
def register_dob():
    r = twiml.Response()

    r.say("What is your date of birth? Please state in the order: year, month, and then date. Press the star key when you're done.")
    r.record(transcribe="true", transcribeCallback="/transcribe_dob", action="/register_phone", finishOnKey="*")
    dob = str(r)
	return str(r)


@app.route("/register_phone", methods=['GET','POST'])
def register_phone():
    r = twiml.Response()

    r.say("What is your phone number? Press the star key when you're done.")
    r.record(transcribe="true", transcribeCallback="/transcribe_phone", action="/register_mc", finishOnKey="*")
    phone = str(r)
	return str(r)


@app.route("/register_mc", methods=['GET','POST'])
def register_mc():
    r = twiml.Response()

    r.say("When was your last menstrual cycle? Please state in the order: year, month, and then date. Press the star key when you're done.")
    r.record(transcribe="true", transcribeCallback="/transcribe_mc", action="/register_secondary", finishOnKey="*")
    lastPeriod = str(r)
	return str(r)
	

@app.route("/register_secondary", methods=['GET','POST'])
def register_secondary():
    r = twiml.Response()

    r.say("What is your secondary contact's phone number? Press the star key when you're done.")
    r.record(transcribe="true", transcribeCallback="/transcribe_secondary", action="/register_address", finishOnKey="*")
    emergency = str(r)
	return str(r)


@app.route("/register_address", methods=['GET','POST'])
def register_address():
    r = twiml.Response()

    r.say("What is your address? Press the star key when you're done.")
    r.record(transcribe="true", transcribeCallback="/transcribe_address", action="/register_done", finishOnKey="*")
    addr = str(r)
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

# Insert new info from registration
dataPerson = {
	'last': last,
	'first': first,
	'addr': addr,
	'phone': phone,
	'emergency': emergency,
	'lastPeriod': date(lastPeriod),
	'dob': date(dob)
}
cursor.execute(addPersonalInfo, dataPerson)
connection.commit()


connection.close() 

if __name__ == "__main__":
	app.run()