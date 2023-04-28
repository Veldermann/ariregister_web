from flask import Blueprint, render_template, request
from ... import getDatabaseConnection

avaleht = Blueprint('avaleht', __name__)

@avaleht.route('/', methods=["GET", "POST"])
def main():
    cursor = getDatabaseConnection()
    cursor.execute("""
        SELECT registration_code, name
        FROM companys
        """)
    data = cursor.fetchall()

    return render_template('avaleht/companies_table.html', data = data)

@avaleht.route('/search', methods=["POST"])
def search():
    if request.method == "POST":
        search_string = request.form.get("search")
        print(search_string)
        
    return f"Python back end recieved : {search_string}"