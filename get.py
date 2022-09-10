from __future__ import print_function

import os.path
import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

scp=['https://www.googleapis.com/auth/calendar']
def  get_evnt(count=10):      
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
            if count<0:
                return 'Invalid Number.Give a positive number.'
            
            service = build('calendar','v3',credentials=creds)
            now=datetime.datetime.utcnow().isoformat() + 'Z'

            events_res = service.events().list(calendarId='primary',timeMin=now, maxResults=count, singleEvents=True, orderBy='startTime').execute()
            events =events_res.get('items', [])
            result=""

            if not events:
                return 'No upcoming events'

            for event in events:
                start= event['start'].get('dateTime', event['start'].get('date'))
                date_to_print= start[0:10]
                time_to_print = start[11:19]
                
                final_date = datetime.datetime.strptime(date_to_print,'%Y-%m-%d').strftime('%d/%m/%Y')
                final_time = datetime.datetime.strptime(time_to_print,'%H:%M:%S').strftime('%I:%M %p')
                result+= (final_date+" "+final_time+" "+event['summary']+"\n")
            return result
        except HttpError as error:
            print("An Error Occurred %s"%error)
            return "Couldn't list event"