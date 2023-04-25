from flask import Flask

app = Flask(__name__)
app.config["SECRET_KEY"] = "supamegaukulele"

def create_app():
    
    from .server.index.index import index
    app.register_blueprint(index, url_prefix="/")
    
    from .server.add_new_company.add_new_company import add_new_company
    app.register_blueprint(add_new_company, url_prefix="/add_new_company")
    
    return app