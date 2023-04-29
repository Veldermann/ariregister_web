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


@add_company.route('/add_shareholder', methods=["POST"])
def addShareholder():
    shareholder_name = request.form.get("shareholder_name")
    share_size = request.form.get("share_size")
    shareholder_code = request.form.get("shareholder_code")
    is_company = request.form.get("is_company")
    total_capital = request.form.get("total_capital")
    total_shareholders_share = request.form.get("total_shareholders_share")
    data = {"error": [], "success": []}

    if len(shareholder_name) < 1:
        data["error"].append("Osaniku nimi peab olema täidetud.")

    if share_size and share_size != "NaN":
        if int(share_size) < 1:
            data["error"].append("Osaniku osa peab olema vähemalt 1€.")
    else:
        data["error"].append("Osaniku osa peab olema vähemalt 1€.")
    
    if is_company == "true":
        if len(shareholder_code) != 7:
            data["error"].append("Osaniku registreerimiskood peab olema 7 numbrit.")
    else:
        if len(shareholder_code) != 11:
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

