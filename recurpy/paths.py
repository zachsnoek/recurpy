import os

RECURPY_PATH = os.path.dirname(os.path.realpath(__file__))
DB = RECURPY_PATH + "/events.db"
CONFIG_FILE = RECURPY_PATH + "/config.yaml"
CREDS_FILE = RECURPY_PATH + "/credentials.json"
TOKEN = RECURPY_PATH + "/token.pickle"