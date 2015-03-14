import datetime
import glob
import logging
import os
import psycopg2
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


def get_list_of_feeds():
    feeds = []

    try:
        income_exports_directory = os.environ["INCOME_EXPORTS_DIRECTORY"]
        for feed in glob.glob(income_exports_directory + "/*.csv"):
            feeds.append(feed)
        return feeds
    except KeyError:
        raise KeyError




def archive_feed(source_path, load_success):
    source_directory = os.path.dirname(source_path)
    source_filename = os.path.basename(source_path)

    if load_success:
        destination_path = os.path.join(source_directory, "archived_exports", source_filename)
    else:
        destination_path = os.path.join(source_directory, "bad_exports", source_filename)

    os.rename(source_path, destination_path)


def psql_call(query, logger):
    con = None
    database = "jake"
    user = "jake"

    try:
        con = psycopg2.connect(database=database, user=user)
        cur = con.cursor()
        cur.execute(query)
        con.commit()
    except psycopg2.DatabaseError as exception:
        logger.critical(exception)
        raise exception
    finally:
        if con:
            con.close()


def truncate_import_table(logger):
    query = """
        TRUNCATE TABLE imp_income
        ;
    """

    psql_call(query, logger)


def import_feed(feed, logger):
    query = """
        COPY imp_income
        FROM '{0}'
        WITH CSV
            HEADER
        ;
    """.format(feed)

    psql_call(query, logger)


def upsert_feed(logger):
    update_query = """
        UPDATE arc_income
        SET
            amount = imp.amount,
            category = imp.category,
            notes = imp.notes,
            reimbursement_category = imp.reimbursement_category,
            feed_source = imp.feed_source
        FROM imp_income imp
        WHERE TO_TIMESTAMP(imp.timestamp, 'DD/MM/YYYY HH24:MI:SS')::TIMESTAMP WITHOUT TIME ZONE = arc_income.timestamp
        ;
    """

    insert_query = """
        INSERT INTO arc_income (
            timestamp,
            amount,
            category,
            notes,
            reimbursement_category,
            feed_source
        ) (
            SELECT
                TO_TIMESTAMP(timestamp, 'DD/MM/YYYY HH24:MI:SS')::TIMESTAMP WITHOUT TIME ZONE,
                amount,
                category,
                notes,
                reimbursement_category,
                feed_source
            FROM imp_income imp
            WHERE NOT EXISTS (
                SELECT 1
                FROM arc_income arc
                WHERE TO_TIMESTAMP(imp.timestamp, 'DD/MM/YYYY HH24:MI:SS')::TIMESTAMP WITHOUT TIME ZONE = arc.timestamp
            )
            AND amount > 0
        )
        ;
    """

    upsert_query = update_query + insert_query

    psql_call(upsert_query, logger)


def main():
    script = Script()
    logger = create_logger(script)

    try:
        logger.info("Determine feeds to be imported.")
        feeds = get_list_of_feeds()
    except KeyError:
        logger.critical("A KeyError has been raised.")
        sys.exit(1)

    error_code = 0

    if feeds:
        logger.info("Feeds have been determined.\n")
    else:
        logger.info("There are no feeds to be imported.\n")

    for feed in feeds:
        try:
            logger.info("Processing feed: {0}".format(feed))
            truncate_import_table(logger)
            logger.info("Import table truncated...")
            import_feed(feed, logger)
            logger.info("Feed imported...")
            upsert_feed(logger)
            logger.info("Feed upserted...")
            archive_feed(feed, True)
            logger.info("Feed archived. Moving to next feed.\n")
        except psycopg2.DatabaseError:
            error_code = 1
            archive_feed(feed, False)
            logger.info("Moving feed to bad folder due to database error. Moving to next feed.\n")

    logger.info("End of script.")
    sys.exit(error_code)

if __name__ == "__main__":
    main()