import logging

status_logger = logging.getLogger('kalinka.DatabaseStatus')


def IsDatabaseHealthy(conn, db):
    status_logger.info("Checking status and health of database")


    status_logger.info("Step one: checking database")
    try:

        status_logger.debug(str(conn.server_info()))
    except Exception as e:
        status_logger.error("Unfortunately, something is wrong with database:{err}".format(err=e))
        return False
    status_logger.info("Step one passed")

    status_logger.info("Step two - does all necessary collections exist?")
    necessaryCollections = ['files', 'networks', 'sets']
    if set(necessaryCollections) != set(db.collection_names()).intersection(necessaryCollections):
        status_logger.error("Failed - init that database or change config.ini.")
        return False
    status_logger.info("Step two passed.")

    return True