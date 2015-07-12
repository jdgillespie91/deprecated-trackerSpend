import os
from datetime import datetime
from utils import export_worksheet


def __get_auth_path():
    auth_directory = os.path.dirname(os.path.realpath(__file__))
    auth_file = 'google_key.json'
    return os.path.join(auth_directory, auth_file)

def __get_workbook_key():
    return '1FqFrrbshmgdEJA1mqABuG_xp8Sc_SdZFjLCgP3DHVzk'

def __get_worksheet_name():
    return 'responses'

def __get_export_path():
    export_directory = os.path.dirname(os.path.realpath(__file__))
    export_file = 'expenditure_export_{0}.json'.format(datetime.today().strftime('%Y-%m-%d_%H:%M:%S'))
    return os.path.join(export_directory, export_file)


if __name__ == '__main__':
    auth_path = __get_auth_path()
    workbook_key = __get_workbook_key()
    worksheet_name = __get_worksheet_name()
    export_path = __get_export_path()
    export_worksheet(auth_path, workbook_key, worksheet_name, export_path)
