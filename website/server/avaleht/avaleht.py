from flask import Blueprint, render_template, request

avaleht = Blueprint('avaleht', __name__)

@avaleht.route('/', methods=["GET", "POST"])
def main():
    
    return render_template('avaleht/avaleht.html')

@avaleht.route('/search', methods=["POST"])
def search():
    if request.method == "POST":
        search_string = request.form.get("search")
        
    return f"Python back end recieved : {search_string}"
