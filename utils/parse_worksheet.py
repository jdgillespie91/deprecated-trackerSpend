import gspread
import json
import os
from oauth2client.client import SignedJwtAssertionCredentials


def __open_worksheet(auth_key_path, workbook_key, worksheet_name):
    with open(auth_key_path) as key:
        json_key = json.load(key)

    credentials = SignedJwtAssertionCredentials(json_key['client_email'], bytes(json_key['private_key'], 'UTF-8'), 'https://spreadsheets.google.com/feeds')
    session = gspread.authorize(credentials)
    workbook = session.open_by_key(workbook_key)
    worksheet = workbook.worksheet(worksheet_name)

    return worksheet

def __get_data():
    pass

def __write_data():
    pass

def parse_worksheet(auth_key_path, workbook_key, worksheet_name):
    worksheet = __open_worksheet(auth_key_path, workbook_key, worksheet_name)

    return worksheet


if __name__ == '__main__':
    auth_key_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'google_key.json')
    workbook_key = '1FqFrrbshmgdEJA1mqABuG_xp8Sc_SdZFjLCgP3DHVzk'
    worksheet_name = 'responses'

    parse_worksheet(auth_key_path, workbook_key, worksheet_name)
