from prettytable import PrettyTable
import recurpy.database as db
import recurpy.input_verification as verify
import recurpy.calendar_manager as cal

def add_to_google(event_id, event_date):
    """Add the event with id event_id on date event_date to the users's Google Calendar."""

    event = db.get_event(event_id)
    if event == None:
        print("ERROR: Could not get event from database.\nRun `recurpy list` to view valid events.")
        exit(1)

    if (verify.verify_date(event_date) == False):
        print("ERROR: Event date is not in correct format. Please enter a date in YYYY-MM-DD format.")
        exit(1)

    cal.add_event(event_date, event)

def list_events():
    """Print the user's stored events as a table."""

    events = db.select_all()
    
    if len(events) == 0:
        print("No events to show. Run 'recurpy new' to add an event.")
    else:
        x = PrettyTable()
        x.field_names = ["ID", "Summary", "Location", "Description", "Start Time", "End Time", "End Date"]
        x.align["Summary"] = "l"
        x.align["Location"] = "l"
        x.align["Description"] = "l"

        for event in events:
            event = list(event)
            x.add_row(["[none]" if e == "" else e for e in event])

        print(x)

def new_event():
    """Ask the user for event information and create a new event in the database."""
    
    # Get event summary
    summary = input("Event summary (name of event): ")
    while summary == "":
        print("Please enter a non-empty value.")
        summary = input("Event summary (name of event): ")

    # Get event location (optional)
    location = input("Event location (optional): ")
    description = input("Event description (optional): ")

    # Get event start time
    start_time = input("Event start time in 24-hr format (HH:MM): ")
    while verify.verify_time(start_time) == False:
        print("Please enter a time formatted as HH:MM.")
        start_time = input("Event start time in 24-hr format (HH:MM): ")

    # Get event end time
    end_time = input("Event end time in 24-hr format (HH:MM): ")
    while verify.verify_time(end_time) == False:
        print("Please enter a time formatted as HH:MM.")
        end_time = input("Event end time in 24-hr format (HH:MM): ")

    # Get event end day (i.e., length of event in days as offset from start time)
    end_date = input("Event end date as offset from start time (optional; default 0): ")
    while end_date != "" and end_date.isdigit() == False:
        print("Please enter an integer end date offset.")
        end_date = input("Event end date as offset from start time (optional; default 0): ")

    # Default end day to 0 (i.e., event starts and ends on the same day)
    if end_date == "":
        end_date = 0

    db.insert((summary, location, description, start_time, end_time, end_date))
    print("\nSuccesfully created new event '{}'.".format(summary))

def delete_event(event_id):
    """Delete the event with id event_id from the database."""

    e = db.get_event(event_id)
    if e == None:
        print("ERROR: Event ID '{}' does not exist.".format(event_id))
        exit(1)

    db.delete(event_id)
    print("Successfully deleted event.")