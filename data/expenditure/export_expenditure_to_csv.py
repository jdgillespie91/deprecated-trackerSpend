# This script adds any expenditure that occurs regularly on a monthly basis.

import csv
import datetime
import gspread
import json
import logging
import os
import sys
from configs import config
from oauth2client.client import SignedJwtAssertionCredentials


class Script:
    def __init__(self):
        self.today = datetime.datetime.today()
        self.directory = os.path.dirname(__file__)
        self.filename = os.path.splitext(os.path.basename(__file__))[0]
        self.path = os.path.join(self.directory, self.filename)


def create_logger(script):
    today = script.today.strftime('%Y-%m-%d_%H:%M:%S')
    directory = os.path.join(script.directory, 'logs')
    filename = '{0}_{1}.log'.format(script.filename, today)
    path = os.path.join(directory, filename)

    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)

    # Add file handler to logger.
    file_handler = logging.FileHandler(path)
    formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.debug('Log file created: {0}\n'.format(path))

    # Add smtp handler to logger.
    # smtp_handler = logging.handlers.SMTPHandler(... # Complete this
    # logger.debug('SMTP functionality configured.')

    return logger


def parse_expenditure_sheet():
    conf = config.Config('expenditure_responses')

    json_key = json.load(open(conf.key))
    scope = ['https://spreadsheets.google.com/feeds']

    credentials = SignedJwtAssertionCredentials(json_key['client_email'], bytes(json_key['private_key'], 'UTF-8'), scope)
    session = gspread.authorize(credentials)

    workbook = session.open_by_key(conf.workbook)
    worksheet = workbook.worksheet(conf.worksheet)
    worksheet_values = worksheet.get_all_values()

    export_directory = os.path.join(os.path.dirname(__file__), 'exports')
    export_filename = 'export_{0}.csv'.format(datetime.datetime.today().strftime('%Y-%m-%d_%H:%M:%S'))
    export_path = os.path.join(export_directory, export_filename)

    # Append feed source to each row in the export.
    for row in worksheet_values:
        row.append(export_filename)

    with open(export_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(worksheet_values)

    return 0


if __name__ == '__main__':
    script = Script()
    logger = create_logger(script)

    logger.info('Start of processing.')
    parse_expenditure_sheet()
    logger.info('End of processing.\n')

    logger.info('End of script.')
    sys.exit(0)
