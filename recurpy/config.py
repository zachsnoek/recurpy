import json, yaml
import recurpy.paths as p
import recurpy.database as db
import recurpy.calendar_manager as cal
import recurpy.input_verification as verify

CONFIG_FILE = "recurpy/config.yaml"

# YAML helper functions

def load_config():
    """Load the configuration file and return as a dictionary."""

    return yaml.safe_load(open(p.CONFIG_FILE, "r"))

def dump_config(config):
    """Write the contents of config to the configuration file."""

    yaml.safe_dump(config, open(p.CONFIG_FILE, "w"), indent=4)

# Configuration functions

def config_db(lone=True):
    """Initialize the database if it doesn't exist."""

    import os

    if os.path.isfile(p.DB):
        print("\nAn events database already exists. Skipping database creation.")
    else:
        db.initialize()
        print("\nCreated new events database.")

        if lone:
            print("Successfully created a new database.")

def config_cal_id(lone=True):
    """Ask the user for a Google Calendar ID and write it to the configuration file."""

    cal_id = input("\nEnter the Google Calendar ID to use: ")
    
    while cal_id == "":
        print("\nPlease enter a Google Calendar ID.")
        cal_id = input("Enter the Google Calendar ID to use: ")

    try:
        config = load_config()
        config["calendar"]["id"] = cal_id
        dump_config(config)

        if lone:
            print("Successfully configured Google Calendar ID.")
    except Exception as e:
        print("ERROR: Error configuring Google Calendar ID.")
        print(e)
        exit(1)

def get_cal_id():
    """Return the Google Calendar ID from the configuration file."""
    return load_config()["calendar"]["id"]

def config_timezone(lone=True):
    """Ask the user for a time zone and write it to the configuration file."""

    time_zone = input("\nEnter your time zone in offset from GMT (e.g., 04:00): ")
    while verify.verify_time(time_zone) == False:
        print("\nPlease enter a time zone.")
        time_zone = input("Enter the time zone in offset from GMT (e.g., 04:00): ")
    
    try:
        config = load_config()
        config["calendar"]["time zone"] = time_zone
        dump_config(config)

        if lone:
            print("Successfully configured time zone.")
    except:
        print("ERROR: Error configuring time zone.")
        exit(1)

def get_timezone():
    """Return the timezone from the configuration file."""

    return load_config()["calendar"]["time zone"] 

def config_credentials(lone=True):
    """Ask the user for their Google OAuth credentials and write them to credentials.json."""

    print('''
To configure your Google OAuth credentials, first go to https://developers.google.com/calendar/quickstart/python.

1. Click 'Enable the Google Calendar API'
2. Select 'Desktop app'
3. Click 'Create'
4. Click 'Download Client Configuration'
5. Copy the content of 'credentials.json' and paste into the prompt below
    ''')

    creds = input("Paste the content of 'credentials.json': ")
    while (creds == ""):
        print("\nPlease input credentials.")
        creds = input("Paste the content of 'credentials.json': ")

    try:
        data = json.loads(creds)
        with open(p.CREDS_FILE, "w") as creds_file:
            json.dump(data, creds_file, indent=4)
        
        if lone:
            print("Credentials configured.")
    except Exception as e:
        print("ERROR: Error saving Google credentials.")
        exit(1)         

def config_auth(lone=True):
    """Authorize this application for the user's Google account if it is not already authorized."""

    try:
        cal.authorize()

        if lone:
            print("Successfully configured Google authorization.")
    except:
        print("ERROR: Error authorizing Google credentials. Check that 'credentials.json' exists.")
        exit(1)

def config_all():
    """Run all of the configuration functions."""

    while True:
        res = input("Attempting a full configuration. Any previous configurations will be overwritten.\nIf an events database exists, it will not be destroyed. Continue? (y/n): ")
        if res.lower() in ["y", "n"]:
            break
        else:
            print("Please type Y or N.")

    if res == "n":
        print("\nAborting configuration.")
        exit()

    config_db(lone=False)
    config_cal_id(lone=False)
    config_timezone(lone=False)
    config_credentials(lone=False)

    print("\nIf necessary, your browser will open in 3 seconds to complete authorization.")
    print("Please complete the steps to authorize this application.\n")
    import time
    time.sleep(3)
    config_auth(lone=False)

    print("\nConfiguration complete.")