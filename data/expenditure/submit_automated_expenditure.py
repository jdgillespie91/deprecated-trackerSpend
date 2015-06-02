# This script adds any spend that occurs regularly on a monthly basis.

import datetime
import gspread
import json
import logging
import os
import requests
import smtplib
import sys
from configs import config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from oauth2client.client import SignedJwtAssertionCredentials


class Script:
    def __init__(self):
        self.today = datetime.datetime.today()
        self.directory = os.path.dirname(__file__)
        self.filename = os.path.splitext(os.path.basename(__file__))[0]
        self.path = os.path.join(self.directory, self.filename)


class Flag(Script):
    def __init__(self, entry):
        Script.__init__(self)  # Change this to super if more pythonic.

        self.today = self.today.strftime('%Y-%m-%d')
        self.directory = os.path.join(self.directory, 'flags')
        self.filename = '{0}_{1}.flag'.format(entry.category, self.today)
        self.path = os.path.join(self.directory, self.filename)

    def exists(self):
        if os.path.isfile(self.path):
            return True
        else:
            return False

    def touch(self):
        open(self.path, 'w').close()

    def untouch(self):
        os.remove(self.path)


class Entry:
    def __init__(self, amount, category, peer_pressure, notes, frequency, due_date, active):
        self.amount = amount
        self.category = category
        self.peer_pressure = peer_pressure
        self.notes = notes
        self.frequency = frequency
        self.due_date = due_date
        self.active = active


class Form:
    def __init__(self, entry):
        self.amount = entry.amount
        self.category = entry.category
        self.peer_pressure = entry.peer_pressure
        self.notes = entry.notes
        self.conf = config.Config('expenditure_form')
        self.submission = {'entry.1788911046': self.amount,
                           'entry.22851461': '__other_option__',
                           'entry.22851461.other_option_response': self.category,
                           'entry.2106932303': self.peer_pressure,
                           'entry.1728679999': self.notes}
        self.response_code = None

    def submit(self):
        response = requests.post(self.conf.url, self.submission)
        self.response_code = response.status_code

    def email(self, success):
        # The following code is based on
        # http://stackoverflow.com/questions/778202/smtplib-and-gmail-python-script-problems
        # http://en.wikibooks.org/wiki/Python_Programming/Email
        # I need to troubleshoot and test for errors.

        message = MIMEMultipart()
        message['From'] = self.conf.sender
        message['To'] = self.conf.recipient
        message['Subject'] = 'Expenditure Submission Update (Automated Email)'

        if success:
            body = 'The following entry has been submitted.\n\nAmount: {0}\nCategory: {1}\nPeer pressure: {2}\n' \
                   'Notes: {3}\n'.format(self.amount, self.category, self.peer_pressure, self.notes)
        else:
            body = 'The following entry failed submission.\n\nAmount: {0}\nCategory: {1}\nPeer pressure: {2}\n' \
                   'Notes: {3}\n'.format(self.amount, self.category, self.peer_pressure, self.notes)

        message.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.conf.username, self.conf.password)
        server.sendmail(self.conf.sender, self.conf.recipient, message.as_string())
        server.close()


# Initialise the Entry class based on a list row.
def create_entry(row):
    category = row[1]
    peer_pressure = row[2]
    notes = row[3]
    frequency = row[4]
    active = True if row[6] == 'Yes' else False

    # We assign zero to both amount and due_date if either are invalid types. We do this silently because the email
    # confirmation will contain the details of the submission and highlight any issues that need to be addressed.
    try:
        amount = float(row[0])
        due_date = int(row[5])
    except (TypeError, ValueError):
        amount = 0
        due_date = 0

    entry = Entry(amount, category, peer_pressure, notes, frequency, due_date, active)

    return entry


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


def parse_entries_sheet():
    conf = config.Config('expenditure_entries')

    json_key = json.load(open(conf.key))
    scope = ['https://spreadsheets.google.com/feeds']

    credentials = SignedJwtAssertionCredentials(json_key['client_email'], bytes(json_key['private_key'], 'UTF-8'), scope)
    session = gspread.authorize(credentials)

    workbook = session.open_by_key(conf.workbook)
    worksheet = workbook.worksheet(conf.worksheet)

    # Parse row-by-row until an empty row is encountered (data starts on second row).
    row_index = 2
    entries = []
    while worksheet.row_values(row_index) and row_index <= worksheet.row_count:
        row = worksheet.row_values(row_index)
        entry = create_entry(row)
        entries.append(entry)
        row_index += 1

    return entries


if __name__ == '__main__':
    script = Script()
    logger = create_logger(script)

    logger.info('Processing entries sheet.')
    entries = parse_entries_sheet()
    logger.info('Entries sheet processed.\n')

    for entry in entries:
        logger.info('Processing entry: {0}.'.format(entry.category))
        if entry.active:
            logger.info('Entry is active. Continuing...')
            flag = Flag(entry)
            if not flag.exists():
                logger.info('The flag file does not exist. Touching...')
                flag.touch()
                if entry.frequency == 'Monthly':
                    if entry.due_date == script.today.day:  # Think about introducing a "today" variable. I don't think it's logical to include "today" in the Script class.
                        logger.info('An entry is required. Submitting...')
                        form = Form(entry)
                        form.submit()
                        if form.response_code == requests.codes.ok:  # Have this as try: form.submit() as opposed to if/else (will read better).
                            logger.info('The submission was accepted. Moving to next entry.\n')
                            form.email(success=True)
                        else:
                            logger.info('The submission was not accepted. '
                                        'Removing flag file and moving to next entry.\n')
                            form.email(success=False)
                            flag.untouch()
                    else:
                        logger.info('A submission is not required today. '
                                    'Removing flag file and moving to next entry.\n'.format(entry.frequency))
                        flag.untouch()
                else:
                    logger.info('{0} spend is not yet implemented. '
                                'Removing flag file and moving to next entry.\n'.format(entry.frequency))
                    flag.untouch()
                    continue
            else:
                logger.info('The flag file exists. Moving to next entry.\n')
        else:
            logger.info('Entry is inactive. Moving to next entry.\n')

    logger.info('End of script.')
    sys.exit(0)
