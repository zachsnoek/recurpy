import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import recurpy.config as config
import recurpy.paths as p

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/calendar"]
CREDENTIALS = p.CREDS_FILE
TOKEN = p.TOKEN

def authorize():
    """Authorize this application if it is not already authorized."""

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN):
        with open(TOKEN, "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN, "wb") as token:
            pickle.dump(creds, token)

    service = build("calendar", "v3", credentials=creds)

    return service

def add_event(event_date, event):
    """
    Add an event to the user's Google Calendar.
    
    Arguments:
    event_date -- the start date of the event formatted as YYYY-MM-DD.
    event -- a tuple containing the summary, location, description, start time, end time, and end date.
    """

    try:
        service = authorize()
    except:
        print("ERROR: could not authorize Google credentials.")
        exit(1)

    try:
        timezone = config.get_timezone()
        end_date_offset = event[5]                                      # get end date offset
        end_date = datetime.datetime.strptime(event_date, "%Y-%m-%d")   # convert event_date to datetime object
        end_date = end_date + datetime.timedelta(days=end_date_offset)  # add date offset
        end_date = end_date.strftime("%Y-%m-%d")                        # convert back to string

        body = {
            "summary": event[0],
            "location": event[1],
            "description": event[2],
            "start": {
                "dateTime": "{}T{}:00-{}".format(event_date, event[3], timezone)
            },
            "end": {
                "dateTime": "{}T{}:00-{}".format(end_date, event[4], timezone)
            },
        }

        ggl_event = service.events().insert(calendarId=config.get_cal_id(), body=body).execute()
        print("Event added to your calendar.")
    except Exception as e:
        print("ERROR: could not add event to Google Calendar.")
        exit(1)