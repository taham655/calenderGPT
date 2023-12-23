from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from dateutil.parser import parse
from datetime import timedelta
from tzlocal import get_localzone
import tzlocal
import os

def add_event(start_time_str, summary, location=None, end_time_str=None, description=None, is_recurring=False, recurrence_rule=None):
    # Define the scope
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    # Authenticate and create a service
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # Parse the start time and handle the timezone
    start_time = parse(start_time_str)
    local_timezone = tzlocal.get_localzone_name()

    if not end_time_str:
        end_time = start_time + timedelta(minutes=15)
        end_time_str = end_time.isoformat()

    # Create the event
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

    # Add the event to the calendar
    created_event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (created_event.get('htmlLink')))

# Example usage of the function
add_event('2023-12-23T23:00:00', 'Meeting with Ahmed', 'Office')
