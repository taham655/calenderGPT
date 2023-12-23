from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from dateutil.parser import parse
from datetime import timedelta
from tzlocal import get_localzone
import tzlocal
import datetime
import os 

class GoogleCalendar:
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    def __init__(self):
        self.service = self.get_calendar_service()

    def get_calendar_service(self):
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return build('calendar', 'v3', credentials=creds)

    def add_event(self, start_time_str, summary, location=None, end_time_str=None, description=None, is_recurring=False, recurrence_rule=None):
        start_time = parse(start_time_str)
        local_timezone = tzlocal.get_localzone_name()

        if not end_time_str:
            end_time = start_time + timedelta(minutes=15)
            end_time_str = end_time.isoformat()

        event = {
            'summary': summary,
            'location': location,
            'description': description,
            'start': {
                'dateTime': start_time_str,
                'timeZone': local_timezone,
            },
            'end': {
                'dateTime': end_time_str,
                'timeZone': local_timezone,
            }
        }

        if is_recurring and recurrence_rule:
            event['recurrence'] = [recurrence_rule]

        created_event = self.service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s' % (created_event.get('htmlLink')))

# Usage
calendar = GoogleCalendar()
calendar.add_event('2023-12-23T07:00:00', summary='Meeting with ahmed bhai', location='Office')

# For a recurring event
# recurrence_rule = 'RRULE:FREQ=WEEKLY;BYDAY=MO'
# calendar.add_event('2023-12-21T8:00:00', '2023-12-21T13:00:00', 'Wake up ', 'Office', 'Team weekly sync-up', is_recurring=True, recurrence_rule=recurrence_rule)
