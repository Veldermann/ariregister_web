from ... import getDatabaseConnection

def getData(result):
    data = []
    for company in result:
        data.append({'id': company[0], 'registration_code': company[1], 'name': company[2]})
    return data

def searchByCompanyName(search_string):
    cursor = getDatabaseConnection()
    cursor.execute("""
        SELECT id, registration_code, name
        FROM company
        WHERE name LIKE %(name)s
        """, {"name" : "%" + search_string + "%"})
    result = cursor.fetchall()
    cursor.close()
    return getData(result)

def searchByRegistrationCode(search_string):
    cursor = getDatabaseConnection()
    cursor.execute("""
        SELECT id, registration_code, name
        FROM company
        WHERE CAST(registration_code as TEXT) LIKE %(registration_code)s
        """, {"registration_code" : "%" + search_string + "%"})
    result = cursor.fetchall()
    cursor.close()
    return getData(result)

def searchByShareholderName(search_string):
    cursor = getDatabaseConnection()
    # Person as shareholder
    cursor.execute("""
        SELECT shares.company_id, company.registration_code, company.name 
        FROM company 
        INNER JOIN (
            SELECT share.company_id 
            FROM person 
            INNER JOIN share 
            ON person.id = share.shareholder_id 
            WHERE person.name LIKE %(name)s) AS shares 
        ON company.id = shares.company_id
        """, {"name" : "%" + search_string + "%"})
    personResult = cursor.fetchall()
    
    # Company as shareholder
    cursor.execute("""
        SELECT shares.company_id, company.registration_code, company.name 
        FROM company 
        INNER JOIN (
            SELECT share.company_id 
            FROM company 
            INNER JOIN share 
            ON company.id = share.shareholder_id 
            WHERE company.name LIKE %(name)s) AS shares 
        ON company.id = shares.company_id
        """, {"name" : "%" + search_string + "%"})
    companyResult = cursor.fetchall()

    # Make list and remove duplicates
    result = list(dict.fromkeys(companyResult + personResult))
    cursor.close()

def searchByIdentificationRegistrationCode(search_string):
    cursor = getDatabaseConnection()
    # Person as shareholder
    cursor.execute("""
        SELECT shares.company_id, company.registration_code, company.name 
        FROM company 
        INNER JOIN (
            SELECT share.company_id 
            FROM person 
            INNER JOIN share 
            ON person.id = share.shareholder_id 
            WHERE CAST(person.identification_number AS TEXT) LIKE %(identification_number)s) AS shares 
        ON company.id = shares.company_id
        """, {"identification_number" : search_string + "%"})
    personResult = cursor.fetchall()
    
    # Company as shareholder
    cursor.execute("""
        SELECT shares.company_id, company.registration_code, company.name 
        FROM company 
        INNER JOIN (
            SELECT share.company_id 
            FROM company 
            INNER JOIN share 
            ON company.id = share.shareholder_id 
            WHERE CAST(company.registration_code AS TEXT) LIKE %(identification_number)s) AS shares 
        ON company.id = shares.company_id
        """, {"identification_number" : search_string + "%"})
    companyResult = cursor.fetchall()

    # Make list and remove duplicates
    result = list(dict.fromkeys(companyResult + personResult))
    cursor.close()
    return getData(result)