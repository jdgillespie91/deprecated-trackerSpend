import gspread
import json
import os
from oauth2client.client import SignedJwtAssertionCredentials


def __open_worksheet(auth_file, workbook_key, worksheet_name):
    with open(auth_file) as key:
        json_key = json.load(key)

    credentials = SignedJwtAssertionCredentials(json_key['client_email'], bytes(json_key['private_key'], 'UTF-8'), 'https://spreadsheets.google.com/feeds')
    session = gspread.authorize(credentials)
    workbook = session.open_by_key(workbook_key)
    worksheet = workbook.worksheet(worksheet_name)

    return worksheet

def __get_data(worksheet):
    return worksheet.get_all_records()

def __write_data(data, file):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

def export_worksheet(auth_file, workbook_key, worksheet_name, out_file):
    """ Create .json export of a Google sheet.

    The Google sheet should contain
    
    """
    worksheet = __open_worksheet(auth_file, workbook_key, worksheet_name)
    data = __get_data(worksheet)
    __write_data(data, out_file)
