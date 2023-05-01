from flask import Blueprint, render_template, request
from ... import getDatabaseConnection

company = Blueprint('company', __name__)

@company.route('/', methods=["GET"])
def main():
    data = {}
    company_id = int(request.args.get('id'))
    cursor = getDatabaseConnection()
    cursor.execute("""
        SELECT *
        FROM company
        WHERE id = %(id)s
        """, {'id': company_id})
    result = cursor.fetchone()
    data["company"] = result

    cursor.execute("""
        SELECT registration_code, name, share.share_size, is_founder
        FROM company 
        INNER JOIN share
        ON company.id = share.shareholder_id
        WHERE share.company_id = %(company_id)s
        AND share.is_company = true
        """, {'company_id': company_id})
    resultCompany = cursor.fetchall()

    cursor.execute("""
        SELECT identification_number, CONCAT(name, ' ', lastname), share.share_size, is_founder
        FROM person 
        INNER JOIN share
        ON person.id = share.shareholder_id
        WHERE share.company_id = %(company_id)s
        AND share.is_company = false
        """, {'company_id': company_id})
    resultPerson = cursor.fetchall()

    data['shareholders'] = resultCompany + resultPerson
    cursor.close()

    return render_template('company/shareholders_list.html', data = data)