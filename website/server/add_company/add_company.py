from flask import Blueprint, render_template, request, flash, redirect
from .form_validator import FormValidator
from .save_company import saveCompany
import math

add_company = Blueprint('add_company', __name__)

@add_company.route('/', methods=["GET", "POST"])
def main():
    if request.method == "POST":
        data = formControll(request)
        return data
        
    return render_template('add_company/add_company.html')


@add_company.route('/add_partner', methods=["POST"])
def addPartner():
    partner_name = request.form.get("partner_name")
    partner_share = request.form.get("partner_share")
    partner_code = request.form.get("partner_code")
    is_company = request.form.get("is_company")
    total_capital = request.form.get("total_capital")
    total_partners_share = request.form.get("total_partners_share")
    data = {"error": [], "success": []}

    if len(partner_name) < 1:
        data["error"].append("Partneri nimi peab olema täidetud.")

    if partner_share and partner_share != "NaN":
        if int(partner_share) < 1:
            data["error"].append("Partneri osa peab olema vähemalt 1€.")
    else:
        data["error"].append("Partneri osa peab olema vähemalt 1€.")
    
    if total_capital:
        if int(total_capital) < 2500:
            data["error"].append("Kogukapital peab olema vähemalt 2500€.")
    else:
        data["error"].append("Kogukapital peab olema vähemalt 2500€.")
    
    if total_partners_share != "NaN":
        if int(total_capital) < int(total_partners_share):
            data["error"].append("Partnerite kogu osa ei tohi olla suurem kui kogukapital.")
    
    if is_company == "true":
        if len(partner_code) != 7:
            data["error"].append("Osaniku registreerimiskood peab olema 7 numbrit.")
    else:
        if len(partner_code) != 11:
            data["error"].append("Isikukood peab olema 11 numbrit.")

    if not data["error"]:
        data["success"].append("Osanik lisatud")
        
    return data

def formControll(data):
    validate_form = FormValidator(data)
    messages = validate_form.validate()
    if not messages["error"]:
        saveCompany(validate_form.validatedData())
        return {"success": ["Ettevõte edukalt lisatud."]}

    return messages

