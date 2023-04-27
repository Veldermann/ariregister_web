from flask import Flask
import psycopg2

def getDatabaseConnection():
    connection = psycopg2.connect(database="ariregister",
                                  user="postgres",
                                  password="+19PorGand78-",
                                  host="127.0.0.1", port="5432")
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

    from .server.company.company import company
    app.register_blueprint(company, url_prefix="/company")
    
    return app