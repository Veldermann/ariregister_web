from flask import Blueprint, render_template, request, flash, redirect
from ... import getDatabaseConnection

search = Blueprint('search', __name__)

@search.route('/search_person_company', methods=["POST"])
def searchPersonCompany():
    if request.method == "POST" and request.form.get('search_string'):
        search_string = request.form.get('search_string')
        search_by = request.form.get('search_by')
        if len(search_string) > 0:
            match search_by:
                case "company_name":
                    return searchByCompanyName(search_string)
                case "registration_code":
                    return searchByRegistrationCode(search_string)
                case "person_name":
                    return searchByPersonName(search_string)
                case "identification_number":
                    return searchByIdentificationNumber(search_string)
    return []

def searchByPersonName(search_string):
    cursor = getDatabaseConnection()
    cursor.execute("""
        SELECT id, identification_number, CONCAT(name, ' ', lastname)
        FROM person
        WHERE CONCAT(name, ' ', lastname) LIKE %(search_string)s
        LIMIT 100
        """, {"search_string": "%" + search_string + "%"})
    result = cursor.fetchall()
    cursor.close()

    return result

def searchByIdentificationNumber(search_string):
    cursor = getDatabaseConnection()
    cursor.execute("""
        SELECT id, identification_number, CONCAT(name, ' ', lastname)
        FROM person
        WHERE CAST(identification_number AS TEXT) LIKE %(search_string)s
        LIMIT 100
        """, {"search_string": search_string + "%"})
    result = cursor.fetchall()
    cursor.close()

    return result

def searchByCompanyName(search_string):
    cursor = getDatabaseConnection()
    cursor.execute("""
        SELECT id, registration_code, name
        FROM company
        WHERE name LIKE %(search_string)s
        LIMIT 100
        """, {"search_string": "%" + search_string + "%"})
    result = cursor.fetchall()
    cursor.close()

    return result

def searchByRegistrationCode(search_string):
    cursor = getDatabaseConnection()
    cursor.execute("""
        SELECT id, registration_code, name
        FROM company
        WHERE CAST(registration_code AS TEXT) LIKE %(search_string)s
        LIMIT 100
        """, {"search_string": search_string + "%"})
    result = cursor.fetchall()
    cursor.close()

    return result