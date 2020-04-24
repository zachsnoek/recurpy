# recurpy
Easily add events with recurring times to your Google Calendar.

## Installation
```bash
$ git clone https://github.com/zachsnoek/recurpy.git
$ cd recurpy
$ pip3 install .
```

## Configuration
### What You'll Need
* A Google account
* The Google Calendar ID that you want to use
* Your GMT timezone offset ([list of offsets](https://en.wikipedia.org/wiki/List_of_UTC_time_offsets))

### Enable the Google Calendar API
1. Go to the [Google Calendar API docs](https://developers.google.com/calendar/quickstart/python)
2. Click "Enable the Google Calendar API"
3. Select "Desktop app"
4. Click "Create"
5. Click "Download Client Configuration"
6. Copy the content of "credentials.json"

Finally, run `recurpy config` to configure your settings:
```bash
$ recurpy config
```

## Creating An Event
To create an event in your database, run `recurpy new`:
```
$ recurpy new
Event summary (name of event): Game Night
Event location (optional): 123 Hasbro Ln. 
Event description (optional): 
Event start time in 24-hr format (HH:MM): 19:00
Event end time in 24-hr format (HH:MM): 22:00
Event end date as offset from start time (optional; default 0): 

Succesfully created new event 'Game Night'.
```

The command will ask you for a summary of the event (the event name), an optional location, an optional description, a start time in 24-hour format, an end time in 24-hour format, and the end date offset from the start time.

The end date offset is the number of days from the start date that the event ends. The default is 0; that is, events start and end on the same day. An end date offset of 3 would mean that the event ends three days after the start date.

## Listing Events
List the events in your database using `recurpy list`:
```
$ recurpy list
+----+------------+----------------+-------------+------------+----------+----------+
| ID | Summary    | Location       | Description | Start Time | End Time | End Date |
+----+------------+----------------+-------------+------------+----------+----------+
| 1  | Game Night | 123 Hasbro Ln. | [none]      |   19:00    |  22:00   |    0     |
+----+------------+----------------+-------------+------------+----------+----------+
```

## Adding an Event to Google Calendar

Run `recurpy add` with the ID of the event and the date to create the event on:
```bash
$ recurpy add 1 2020-04-20
Event successfully added to your calendar.
```