from datetime import date, datetime
from ... import getDatabaseConnection

class FormValidator:
    def __init__(self, data):
        self.data = {}
        self.company_name = data.form.get("company_name")
        self.registration_code = data.form.get("registration_code")
        self.registration_date = data.form.get('registration_date')
        self.total_capital = data.form.get("total_capital")
        self.partners = {}

        first = True
        partner_name = ""
        partner_share = ""
        for field in data.form:
            if "partners" in field and first == True:
                partner_name = data.form.get(field)
                first = False
                continue
            
            if "partners" in field and first == False:
                partner_share = data.form.get(field)
                self.partners[partner_name] = partner_share
                partner_name = ""
                partner_share = ""
                first = True
                continue



    def validate(self):
        data = {"error": [], "success": []}
        today = date.today()
        partners_total_share = 0
        for partner, share in self.partners.items():
            partners_total_share += int(share)

        if self.company_name:
            """
            SELECT name FROM companys WHERE name = self.company_name 
            """

            # if select.count > 0:
            # data["error"].append("Sellise nimega ettevõte on juba registrerritud.")
            if len(self.company_name) < 3:
                data["error"].append("Ettevõte nimi peab olema vähemalt 3 tähemäki pikk, kuid mitte pikem kui 100 tähemärki.")
        else:
            data["error"].append("Ettevõtte nimi peab olema täidetud.")

        if self.registration_code:
            if len(self.registration_code) != 7:
                data["error"].append("Registrikood peab olema täpselt 7 numbrit pikk.")
            if self.registration_code.isnumeric() != True:
                data["error"].append("Registrikood tohib sisaldada ainult numbreid.")

        else:
            data["error"].append("Registrikood peab olema täidetud.")

        if not self.registration_date:
            data["error"].append("Palun vali asutamise kuupäev.")

        if self.total_capital and self.total_capital != "NaN":
            if int(self.total_capital) < 2500:
                data["error"].append("Lubatud minimaalne kogukapitali summa on 2500€.")
        else:
            data["error"].append("Palun täida kogukaptali väli.")

        if len(self.partners.items()) < 1:
            data["error"].append("Palun lisa vähemalt üks osanik")

        # This have calculating error somewhere, take a look asap
        if int(self.total_capital) != partners_total_share:
            data["error"].append("Osanikude osade summa peab võrduma kogukapitaliga.")
        
        if not data["error"]:
            print("No errors encountered")

        return data
    
    def validatedData(self):
        share_holder_ids = []
        holders_into_shares = {}
        for partner, share in self.partners.items():
            share_holder_id = self.getShareHolderId(partner)
            share_holder_ids.append(share_holder_id)
            holders_into_shares[share_holder_id] = {"name": partner, "share": share} 

        validated_data = {"company_name": self.company_name,
                "registration_code": self.registration_code,
                "registration_date": self.registration_date,
                "total_capital": self.total_capital,
                "holders_into_shares": holders_into_shares,
                "share_holder_ids": share_holder_ids
                }
        print(validated_data)
        return validated_data
    
    def getShareHolderId(self, share_holder):
        cursor = getDatabaseConnection()
        cursor.execute("""
            SELECT id
            FROM share_holders
            WHERE name = %(name)s
            """, {"name": share_holder})
        result = cursor.fetchall()
        if len(result) > 0:
            return result[0][0]
        
        cursor.execute("""
            INSERT INTO share_holders(name)
            VALUES (%(name)s)
            """, {"name": share_holder})
        
        cursor.execute("""
            SELECT id
            FROM share_holders
            WHERE name = %(name)s
            """, {"name": share_holder})
        result = cursor.fetchall()

        return result[0][0]
