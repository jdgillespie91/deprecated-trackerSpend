# This script adds any expenditure that occurs regularly on a monthly basis.

import configparser
import csv
import datetime
import gspread
import logging
import os
import sys


class Script:
    def __init__(self):
        self.today = datetime.datetime.today()
        self.directory = os.path.dirname(__file__)
        self.filename = os.path.splitext(os.path.basename(__file__))[0]
        self.path = os.path.join(self.directory, self.filename)


def create_logger(script):
    today = script.today.strftime("%Y-%m-%d_%H:%M:%S")
    directory = os.path.join(script.directory, "logs")
    filename = "{0}_{1}.log".format(script.filename, today)
    path = os.path.join(directory, filename)

    logger = logging.getLogger("logger")
    logger.setLevel(logging.DEBUG)

    # Add file handler to logger.
    file_handler = logging.FileHandler(path)
    formatter = logging.Formatter("%(asctime)s %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.debug("Log file created: {0}\n".format(path))

    # Add smtp handler to logger.
    # smtp_handler = logging.handlers.SMTPHandler(... # Complete this
    # logger.debug("SMTP functionality configured.")

    return logger


def parse_config():
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), "resources", "config.ini"))

    username = config.get("expenditure_responses", "username")
    password = config.get("expenditure_responses", "password")
    workbook = config.get("expenditure_responses", "workbook")
    worksheet = config.get("expenditure_responses", "worksheet")

    return username, password, workbook, worksheet


def parse_expenditure_sheet():
    username, password, workbook, worksheet = parse_config()

    session = gspread.login(username, password)
    workbook = session.open_by_key(workbook)
    worksheet = workbook.worksheet(worksheet)

    worksheet_values = worksheet.get_all_values()

    export_directory = os.path.join(os.path.dirname(__file__), "exports")
    export_filename = "{0}_{1}.csv".format("export", datetime.datetime.today().strftime("%Y-%m-%d_%H:%M:%S"))
    export_path = os.path.join(export_directory, export_filename)

    # Append feed source to each row in the export.
    for row in worksheet_values:
        row.append(export_filename)

    print(worksheet_values)

    with open(export_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(worksheet_values)

    return 0


def main():
    script = Script()
    logger = create_logger(script)

    logger.info("Processing expenditure sheet.")
    parse_expenditure_sheet()
    logger.info("Expenditure sheet processed.\n")

    logger.info("End of script.")
    sys.exit(0)

if __name__ == "__main__":
    main()
