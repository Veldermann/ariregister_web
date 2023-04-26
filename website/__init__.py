from flask import Flask

app = Flask(__name__)
app.config["SECRET_KEY"] = "supamegaukulele"

def create_app():
    
    from .server.avaleht.avaleht import avaleht
    app.register_blueprint(avaleht, url_prefix="/")
    
    from .server.add_company.add_company import add_company
    app.register_blueprint(add_company, url_prefix="/add_company")
    
    return app