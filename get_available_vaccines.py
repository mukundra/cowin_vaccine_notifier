import datetime
import json

import requests
from twilio.rest import Client

# set env variable
# after setting up twilio account using - https://www.twilio.com/blog/send-whatsapp-message-30-seconds-python
# export TWILIO_ACCOUNT_SID='ACxxxxxxxx' # paste in Account SID between single quotes
# u can use mine if not many people are using it
# export TWILIO_AUTH_TOKEN='secret auth token' # paste Auth Token between single quotes

# change district id, u can get district ids
# by running following commands
# get state id - curl -X GET "https://cdn-api.co-vin.in/api/v2/admin/location/states" -H "accept: application/json" -H "Accept-Language: hi_IN"
# example dtate id is 31 for tamil nadu
# get district ids by -
# curl -X GET "https://cdn-api.co-vin.in/api/v2/admin/location/districts/31" -H "accept: application/json" -H "Accept-Language: hi_IN"
# choose ur district
district_id = 571

# change age
age = 18

# change your whatsapp number
whatsapp_nos = ['+919444250057']


def send_whatsapp_message(msg):
    # client credentials are read from TWILIO_ACCOUNT_SID and AUTH_TOKEN
    client = Client()

    # this is the Twilio sandbox testing number
    from_whatsapp_number = 'whatsapp:+14155238886'
    # replace this number with your own WhatsApp Messaging number
    for whatsapp in whatsapp_nos:
        to_whatsapp_number = 'whatsapp:{whatsapp_no}'.format(whatsapp_no=whatsapp)
        client.messages.create(body=msg,
                               from_=from_whatsapp_number,
                               to=to_whatsapp_number)


def get_available_slots(district, date, age):
    response = requests.get(
        "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={district}&date={date}".format(
            district=district, date=date))
    # try:
    sessions = json.loads(response.text)
    # except:
    #     return []
    available_slots = []
    for session in sessions['sessions']:
        print("checking slot: " + str(session))
        min_age = int(session['min_age_limit'])
        if (min_age <= age):
            available_capacity = session['available_capacity']
            if (available_capacity > 0):
                print("Available slot: "+str(session))
                available_slots.append(session)
    return available_slots


available_slots = []
for i in range(30):
    date = (datetime.datetime.today() + datetime.timedelta(days=i)).strftime('%d-%m-%Y')
    available_slots += get_available_slots(district_id, date, 18)

now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
if len(available_slots)>0:
    print("slots available  " + str(available_slots) + str(now))
    send_whatsapp_message(str(available_slots))
else:
    print("no slots available " + str(now))
