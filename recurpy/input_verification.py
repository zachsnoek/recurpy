import datetime as datetime

def verify_time(time):
    """Verify that time is formatted as HH:MM."""

    try:
        datetime.datetime.strptime(time, "%H:%M")
        return True
    except ValueError:
        return False

def verify_date(date):
    """Verify that date is formatted as YYYY-MM-DD."""

    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False