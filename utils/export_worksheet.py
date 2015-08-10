import gspread
import json
import os
from oauth2client.client import SignedJwtAssertionCredentials


def __get_worksheet(auth_file, workbook_key, worksheet_name):
    with open(auth_file) as key:
        json_key = json.load(key)

    credentials = SignedJwtAssertionCredentials(json_key['client_email'],
                                                bytes(json_key['private_key'], 'UTF-8'),
                                                'https://spreadsheets.google.com/feeds')
    session = gspread.authorize(credentials)
    workbook = session.open_by_key(workbook_key)
    worksheet =  workbook.worksheet(worksheet_name)
    
    return worksheet.get_all_records()

def __write_data(data, file):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

def export_worksheet(auth_file, workbook_key, worksheet_name, out_file):
    """ Create .json export of a Google sheet.

    The Google sheet should contain a single header row and corresponding values underneath.
    The export will contain a list of dictionaries where each item in the list is a
    dictionary whose keys are the headers and whose values are the corresponding values
    from a single row.

    :param auth_file: Path of authentication file.
    :param workbook_key: Workbook key.
    :param worksheet_name: Worksheet name.
    :param out_file: Path of desired export file.

    Usage::

    >>> from utils import export_worksheet
    >>> export_worksheet('/path/to/auth/file', 'workbook_key', 'worksheet_name', '/path/to/out/file')

    """
    data = __get_data(auth_file, workbook_key, worksheet_name)
    __write_data(data, out_file)
