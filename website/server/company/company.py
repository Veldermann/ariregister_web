from flask import Blueprint, render_template, request
from ... import getDatabaseConnection

company = Blueprint('company', __name__)

@company.route('/', methods=["GET"])
def main():
    registration_code = int(request.args.get("registration_code"))
    print(registration_code)
    return render_template('company/company.html')

"""
@avaleht.route('/search', methods=["POST"])
def search():
    if request.method == "POST":
        search_string = request.form.get("search")
        print(search_string)
        
    return f"Python back end recieved : {search_string}"
"""