from ... import getDatabaseConnection

def saveCompany(data):
    cursor = getDatabaseConnection()

    cursor.execute("""
                INSERT INTO company(registration_code, name, total_capital, date_established)
                VALUES (%(registration_code)s, %(name)s, %(total_capital)s, %(date_established)s)
                RETURNING id
                """, {"registration_code": data["registration_code"], "name": data["name"], "total_capital": data["total_capital"], "date_established": data["date_established"]})
    result = cursor.fetchone()

    for shareholder_id in data["shareholders"]:
        cursor.execute("""
            INSERT INTO share(company_id, shareholder_id, share_size, is_founder, is_company)
            VALUES (%(company_id)s, %(shareholder_id)s, %(share_size)s, %(is_founder)s, %(is_company)s)
            """, {"company_id": result[0], "shareholder_id": shareholder_id, "share_size": data["shareholders"][shareholder_id]["share_size"], "is_founder": "true", "is_company": data["shareholders"][shareholder_id]["is_company"]})
    cursor.close()

    return result[0]