from flask import Blueprint, render_template, request, flash, redirect

add_company = Blueprint('add_company', __name__)

@add_company.route('/', methods=["GET", "POST"])
def launch():
    if request.method == "POST":
        company_name = request.form.get("company-name")
        registration_code = request.form.get("registration-code")
        flash("Ettevõte lisatud", category="success")
        return redirect('/')
        
    return render_template('add_company/add_company.html')

@add_company.route('/add_partner', methods=["POST"])
def addPartner():
    partner_name = request.form.get("partner_name")
    partner_share = request.form.get("partner_share")
    print(type(partner_name))
    print(type(partner_share))
    data = {"error": {}}
    if len(partner_name) < 1:
        data["error"]["partner_name"] = "Partneri nimi peab olema täidetud"
        flash("error", category="success")

    if partner_share:
        if int(partner_share) < 1:
            data["error"]["partner_share"] = "Partneri osa peab olema vähemalt 1€"
    else:
        data["error"]["partner_share"] = "Partneri osa peab olema vähemalt 1€"
    
    return data



