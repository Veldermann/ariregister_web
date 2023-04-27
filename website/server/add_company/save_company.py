from ... import getDatabaseConnection

def saveCompany(data):
    cursor = getDatabaseConnection()

    cursor.execute("""
                INSERT INTO companys(registration_code, name, total_capital, registration_date, share_holders, owners)
                VALUES (%(registration_code)s, %(name)s, %(total_capital)s, %(registration_date)s, %(share_holders)s, %(owners)s)
                """, {"registration_code": data["registration_code"], "name": data["company_name"], "total_capital": data["total_capital"], "registration_date": data["registration_date"], "share_holders": data["share_holder_ids"], "owners": data["share_holder_ids"]})
    
    for share_holder_id in data["share_holder_ids"]:
        cursor.execute("""
            INSERT INTO shares(holder_id, company_id, share_size)
            VALUES (%(holder_id)s, %(company_id)s, %(share_size)s)
            """, {"holder_id": share_holder_id, "company_id": data["registration_code"], "share_size": data["holders_into_shares"][share_holder_id]["share"]})

    return