from flask import Blueprint, render_template, request
from ... import getDatabaseConnection

company = Blueprint('company', __name__)

@company.route('/', methods=["GET"])
def main():
    registration_code = int(request.args.get("registration_code"))
    cursor = getDatabaseConnection()
    cursor.execute("""
        SELECT *
        FROM company
        WHERE registration_code = %(registration_code)s
        """, {"registration_code": registration_code})
    result = cursor.fetchone()

    cursor.close()

    return render_template('company/company.html', data = result)

"""
@avaleht.route('/search', methods=["POST"])
def search():
    if request.method == "POST":
        search_string = request.form.get("search")
        print(search_string)
        
    return f"Python back end recieved : {search_string}"
"""