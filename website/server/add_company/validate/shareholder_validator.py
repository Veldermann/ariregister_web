from flask import Blueprint, render_template, request, flash, redirect

add_shareholder = Blueprint('add_shareholder', __name__)

@add_shareholder.route('/add_shareholder', methods=["POST"])
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