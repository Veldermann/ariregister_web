import configparser
import psycopg2

def getDatabaseConnection():
    config = configparser.ConfigParser()
    config.read('CONFIG.INI')

    connection = psycopg2.connect(database="ariregister",
                                  user=config['database']['username'],
                                  password=config['database']['password'],
                                  host=config['database']['host'], port=config['database']['port'])
    cursor = connection.cursor()
    connection.set_session(autocommit=True)
    return cursor
