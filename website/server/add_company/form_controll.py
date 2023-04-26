
class FormControll:
    def __init__(self, data):
        self.company_name = data.form.get("company_name")
        self.registration_code = data.form.get("registration_code")
        self.registration_date = data.form.get("registration_date")
        self.total_capital = data.form.get("total_capital")
        self.partners = data.form.get("partners")
        
        print(self.partners)
    
    