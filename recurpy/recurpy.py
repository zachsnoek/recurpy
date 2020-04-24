"""
recurpy:
    Easily add events with recurring times to your Google Calendar.

Usage:
    recurpy add <id> <date>
    recurpy list
    recurpy new
    recurpy delete <id>
    recurpy config [--calendar | --timezone | --google]
    recurpy (-h | --help)
    recurpy --version

Commands:
    add         add a new occurence of event <id> on <date> (as YYYY-MM-DD)
    list        list the stored events
    new         create a new event
    delete      delete the event identified by <id>
    config      run recurpy configuration

Options:
    --calendar  only configure the Google Calendar ID
    -h --help   shows this screen
    --google    only configure Google credentials and authorization
    --timezone  only configure the timezone
    --version   shows this version of recurpy
"""
from docopt import docopt
import recurpy.event_manager as em
import recurpy.config as config

def main():
    """Parse the user's argument(s) and call the appropriate functions."""

    args = docopt(__doc__, version="recurpy 0.0.1")

    if args["add"]:
        em.add_to_google(args["<id>"], args["<date>"])
    elif args["list"]:
        em.list_events()
    elif args["new"]:
        em.new_event()
    elif args["delete"]:
        em.delete_event(args["<id>"])
    elif args["config"]:
        if args["--calendar"]:
            config.config_cal_id()
        elif args["--timezone"]:
            config.config_timezone()
        elif args["--google"]:
            config.config_google()
        else:
            config.config_all()

if __name__ == '__main__':
    main()