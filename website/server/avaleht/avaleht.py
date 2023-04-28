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
    cursor.close()

    return render_template('avaleht/companies_table.html', data = data)

@avaleht.route('/search', methods=["POST"])
def search():
    if request.method == "POST":
        data = []
        search_by = request.form.get("search-by")
        search_string = request.form.get("search")
        cursor = getDatabaseConnection()
        cursor.execute("""
            SELECT *
            FROM companys
            WHERE name LIKE %(name)s
            """, {"name" : "%" + search_string + "%"})
        result = cursor.fetchall()
        for company in result:
            data.append({company[0]: company[1]})
        cursor.close()
        
    return data
