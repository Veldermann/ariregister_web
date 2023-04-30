from flask import Flask
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

app = Flask(__name__)
app.config["SECRET_KEY"] = "supamegaukulele"

def create_app():
    
    from .server.avaleht.avaleht import avaleht
    app.register_blueprint(avaleht, url_prefix="/")
    
    from .server.add_company.add_company import add_company
    app.register_blueprint(add_company, url_prefix="/add_company")

    from .server.add_company.validate.shareholder_validator import add_shareholder
    app.register_blueprint(add_shareholder, url_prefix="/add_company")
    from .server.add_company.search_person_company import search
    app.register_blueprint(search, url_prefix="/add_company")

    from .server.company.company import company
    app.register_blueprint(company, url_prefix="/company")

    return app

