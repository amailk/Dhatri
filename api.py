# API
import mysql.connector
from twilio.rest import TwilioRestClient 
 
# put your own credentials here 
ACCOUNT_SID = "AC88e6e50d5cf1fa6e90137c29dc2b1ad5" 
AUTH_TOKEN = "118a797d9a3a376cae56b1ab0ed34497" 
 
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
 
client.messages.create(
    to="+19059660696", 
    from_="+15017250604", 
    body="Test SMS", 
)
