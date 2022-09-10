from __future__ import print_function

import os.path
import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

scp=['https://www.googleapis.com/auth/calendar']
def  crt_evnt(start_date,start_time,end_date,end_time,event_name):
        start_date=datetime.datetime.strptime(start_date, '%d-%b-%y').strftime('%Y-%m-%d')
        end_date=datetime.datetime.strptime(end_date, '%d-%b-%y').strftime('%Y-%m-%d')

        start_time=datetime.datetime.strptime(start_time, '%I:%M%p').strftime('%H:%M:'+'00')
        end_time=datetime.datetime.strptime(end_time, '%I:%M%p').strftime('%H:%M:'+'00')

        event={
            'summary' : event_name,
            'location' : 'NIT Durgapur',
            'start' : {
                'dateTime' : f'{start_date}T{start_time}',
                'timeZone' : 'Asia/Kolkata',
            },
            'end' : {
                'dateTime' : f'{end_date}T{end_time}',
                'timeZone' : 'Asia/Kolkata',
            },
            'recurrence' : [
                'RRULE:FREQ=DAILY;COUNT=1'
            ],
            'reminders':{
                'useDefault' : False,
                'overrides' :[
                    {'method':'email','minutes':24*60},
                    {'method':'popup','minutes':10},
                ],
            },
        }
        
        creds=None

        if os.path.exists('token.json'):
            creds=Credentials.from_authorized_user_file('token.json',scp)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scp)
                creds = flow.run_local_server(port=0)
            with open("token.json","w") as token :
                token.write(creds.to_json())
        try:
            service = build('calendar','v3',credentials=creds)
            events = service.events().insert(calendarId='primary',body=event).execute()
            print("Event Created: %s" %(events.get('htmlLink')))
            return "Congratulations!!! Event Created successfully!!!"
        except HttpError as error:
            print("An Error Occurred %s"%error)
            return "Couldn't create event"