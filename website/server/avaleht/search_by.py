from ... import getDatabaseConnection

def getData(result):
    data = []
    for company in result:
        data.append({company[0]: company[1]})
    return data

def searchByCompanyName(search_string):
    data = []
    cursor = getDatabaseConnection()
    cursor.execute("""
        SELECT *
        FROM companys
        WHERE name LIKE %(name)s
        """, {"name" : "%" + search_string + "%"})
    result = cursor.fetchall()
    cursor.close()
    return getData(result)

def searchByRegistrationCode(search_string):
    data = []
    cursor = getDatabaseConnection()
    cursor.execute("""
        SELECT *
        FROM companys
        WHERE CAST(registration_code as TEXT) LIKE %(registration_code)s
        """, {"registration_code" : "%" + search_string + "%"})
    result = cursor.fetchall()
    cursor.close()
    return getData(result)

def searchByShareholderName(search_string):
    data = []
    cursor = getDatabaseConnection()
    cursor.execute("""
        SELECT company.registration_code, company.name
        FROM share_holders 
        INNER JOIN (
            SELECT registration_code, name, unnest(share_holders) AS shareholder 
            FROM companys) 
            AS company 
        ON share_holders.id = company.shareholder 
        WHERE share_holders.name LIKE %(shareholder_name)s
        GROUP BY company.registration_code, company.name
        """, {"shareholder_name" : "%" + search_string + "%"})
    result = cursor.fetchall()
    cursor.close()
    return getData(result)

def searchByPersonalCode(search_string):
    data = []
    cursor = getDatabaseConnection()
    cursor.execute("""
        SELECT company.registration_code, company.name
        FROM share_holders 
        INNER JOIN (
            SELECT registration_code, name, unnest(share_holders) AS shareholder 
            FROM companys) 
            AS company 
        ON share_holders.id = company.shareholder 
        WHERE CAST(share_holders.id as TEXT) LIKE %(personal_code)s
        GROUP BY company.registration_code, company.name
        """, {"personal_code" : "%" + search_string + "%"})
    result = cursor.fetchall()
    cursor.close()
    return getData(result)