from flask import Blueprint, render_template, request

index = Blueprint('index', __name__)

@index.route('/', methods=["GET", "POST"])
def launch():
    
    return render_template('index/index.html')

@index.route('/search', methods=["POST"])
def search():
    if request.method == "POST":
        search_string = request.form.get("search")
        
    return f"Python back end recieved : {search_string}"
