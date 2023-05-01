from datetime import date, datetime
from .... import getDatabaseConnection

class FormValidator:
    def __init__(self, data):
        print(data.form)
        self.company_name = data.form.get('company_name')
        self.registration_code = data.form.get('registration_code')
        self.date_established = data.form.get('date_established')
        self.total_capital = data.form.get('total_capital')
        self.shareholders = {}
        
        shareholder_id = 0
        share_size = 0
        is_company = False

        count = 0
        for field in data.form:
            if 'shareholders' in field and count == 0:
                shareholder_id = data.form.get(field)
                count += 1
                continue
            
            if 'shareholders' in field and count == 1:
                share_size = data.form.get(field)
                count += 1
                continue

            if 'shareholders' in field and count == 2:
                is_company = data.form.get(field)
                self.shareholders[shareholder_id] = {'share_size': share_size, 'is_company': is_company}
                shareholder_id = 0
                share_size = 0
                is_company = False
                count = 0
                continue

    def validate(self):
        cursor = getDatabaseConnection()
        data = {"error": [], "success": []}
        today = date.today()
        shareholders_total_share = 0

        for shareholder_id, shareholder_data in self.shareholders.items():
            shareholders_total_share += int(self.shareholders[shareholder_id]['share_size'])

        if self.company_name:
            if len(self.company_name) < 3:
                data["error"].append("Ettevõte nimi peab olema vähemalt 3 tähemäki pikk, kuid mitte pikem kui 100 tähemärki.")
            else:
                cursor.execute("""
                    SELECT name
                    FROM company
                    WHERE name = %(name)s
                    """, {'name': self.company_name})
                result = cursor.fetchone()
                if result:
                    data["error"].append("Sellise nimega ettevõte on juba registreeritud.")
        else:
            data["error"].append("Ettevõtte nimi peab olema täidetud.")

        if self.registration_code:
            if len(self.registration_code) != 7:
                data["error"].append("Registrikood peab olema täpselt 7 numbrit pikk.")
            if self.registration_code.isnumeric() != True:
                data["error"].append("Registrikood tohib sisaldada ainult numbreid.")

            cursor.execute("""
                SELECT registration_code
                FROM company
                WHERE CAST(registration_code AS TEXT) = %(registration_code)s
                """, {'registration_code': self.registration_code})
            result = cursor.fetchone()
            if result:
                data["error"].append("Sellise registrikoodiga ettevõte on juba olemas.")

        else:
            data["error"].append("Registrikood peab olema täidetud.")

        if not self.date_established:
            data["error"].append("Palun vali asutamise kuupäev.")

        if self.total_capital and self.total_capital != "NaN":
            if int(self.total_capital) < 2500:
                data["error"].append("Lubatud minimaalne kogukapitali summa on 2500€.")
        else:
            data["error"].append("Palun täida kogukaptali väli.")

        if len(self.shareholders.items()) < 1:
            data["error"].append("Palun lisa vähemalt üks osanik")

        if int(self.total_capital) != shareholders_total_share:
            data["error"].append("Osanikude osade summa peab võrduma kogukapitaliga.")
        
        cursor.close()
        return data
    
    def validatedData(self):
        validated_data = {"registration_code": self.registration_code,
                "name": self.company_name,
                "date_established": self.date_established,
                "total_capital": self.total_capital,
                "shareholders": self.shareholders
                }
        return validated_data
