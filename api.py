# API
import pdb
import mysql.connector
from twilio.rest import TwilioRestClient 
 
# connecting to database
connection = mysql.connector.connect(user='user', password='dhatri', host='127.0.0.1', database='dhatri') 
cursor = connection.cursor()

addPersonalInfo = ("INSERT INTO personal_information "
			"(LastName, FirstName, Address, PhoneNumber, EmergencyNumber, LastMenstrualCycle, DateOfBirth) "
			"VALUES (%(last)s, %(first)s, %(addr)s, %(phone)s, %(emergency)s, %(lastPeriod), %(dob)s")
			
addMidwifeInfo = ("INSERT INTO midwif_information "
			"(LastName, FirstName, FirstWorkDay, LastWorkDay, FirstWorkHour, LastWorkHour) "
			"VALUES (%(last)s, %(first)s, %(firstDay)s, %(LastDay)s, %(FirstHour)s, %(lastHour)")
			
addAppointment = ("INSERT INTO appointments "
			"(PatientFirstName, PatientLastName, PatientPhoneNumber, MidwifeFirstName, MidwifeLastName, MidwifePhoneNumber, Address, DateAndTime) "
			"VALUES (%(patFirst)s, %(patLast)s, %(patPhone)s, %(midFirst)s, %(midLast)s, %(midPhone), %(addr)s, %(dateAndTime)s")

# put your own credentials here 
ACCOUNT_SID = "AC88e6e50d5cf1fa6e90137c29dc2b1ad5" 
AUTH_TOKEN = "118a797d9a3a376cae56b1ab0ed34497" 
 
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
 
client.messages.create(
    to="+19059660696", 
    from_="+12264002125 ", 
    body="Test SMS", 
)

# User Registration

# Midwife Registration

# Setting appointments




connection.commit()
connection.close() 