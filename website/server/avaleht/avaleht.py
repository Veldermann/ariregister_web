from flask import Blueprint, render_template, request
from ... import getDatabaseConnection
from .search_by import *

avaleht = Blueprint('avaleht', __name__)

@avaleht.route('/', methods=["GET", "POST"])
def main():
    cursor = getDatabaseConnection()
    cursor.execute("""
        SELECT registration_code, name
        FROM companys
        """)
    data = cursor.fetchall()
    cursor.close()

    return render_template('avaleht/companies_table.html', data = data)

@avaleht.route('/search', methods=["POST"])
def search():
    if request.method == "POST":
        search_string = request.form.get("search")
        search_by = request.form.get("search-by")
        match search_by:
            case "company_name":
                data = searchByCompanyName(search_string)
            case "registration_code":
                data = searchByRegistrationCode(search_string)
            case "shareholder_name":
                data = searchByShareholderName(search_string)
            case "presonal_code":
                data = searchByPersonalCode(search_string)
    return data