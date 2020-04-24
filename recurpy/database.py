import sqlite3
from sqlite3 import Error
import recurpy.paths as p

DB = p.DB # get the path to the database

def initialize():
    """Connect to the database and create an 'events' table if it doesn't exist."""

    try:
        conn = connect(DB)
        c = conn.cursor()
        c.execute('''
        CREATE TABLE events ( 
            summary VARCHAR(50), 
            location VARCHAR(50), 
            description VARCHAR(50),
            start_time VARCHAR(10), 
            end_time VARCHAR(10),
            end_date INTEGER
        )'''
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print("ERROR: Error creating new table.")
        exit(1)

def connect(db):
    """Return a connection to the database."""

    connection = None

    try:
        connection = sqlite3.connect(db)
    except Error as e:
        print(e)
        exit(1)
        
    return connection

def insert(event):
    """
    Insert an event into the database.
    
    Arguments:
    event -- a tuple containing the summary, location, description, start time, end time, and end date.
    """

    try:
        conn = connect(DB)
        c = conn.cursor()
        c.execute('''
        INSERT INTO events 
        (summary, location, description, start_time, end_time, end_date)
        VALUES (?,?,?,?,?,?)''', event
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print("ERROR: Error inserting new event.")
        exit(1)

def select_all():
    """Return all rows from the database."""

    try:
        conn = connect(DB)
        c = conn.cursor()
        c.execute('''
            SELECT ROWID as ID, summary as Summary, location as Location,
                description as Description, start_time as 'Start Time',
                end_time as 'End Time', end_date as 'End Date'
            FROM events
        ''')
        events = c.fetchall()
        conn.close()
        return events
    except:
        print("ERROR: Error getting events from database.")
        exit(1)

def delete(event_id):
    """Delete the row from the database with id event_id."""

    try:
        conn = connect(DB)
        c = conn.cursor()
        c.execute("DELETE from events WHERE ROWID=?", (int(event_id),))
        conn.commit()
        c.execute("VACUUM")
        conn.commit()
        conn.close()
    except Exception as e:
        print("ERROR: Error deleting event with ID '{}' from database.".format(event_id))
        exit(1)

def get_event(event_id):
    """Return the event from the database with id event_id"""

    try:
        conn = connect(DB)
        c = conn.cursor()
        c.execute("SELECT * from events WHERE ROWID=?", (int(event_id),))
        event = c.fetchone()
        conn.close()
        return event
    except Exception as e:
        print("ERROR: Error getting event from database with ROWID {}".format(event_id))
        exit(1)