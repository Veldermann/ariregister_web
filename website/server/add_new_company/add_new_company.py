from flask import Blueprint, render_template, request, flash, redirect

add_new_company = Blueprint('add_new_company', __name__)

@add_new_company.route('/', methods=["GET", "POST"])
def launch():
    if request.method == "POST":
        company_name = request.form.get("company-name")
        registration_code = request.form.get("registration-code")
        flash("Ettevõte lisatud", category="success")
        return redirect('/')
        
    return render_template('add_new_company/add_new_company.html')

@add_new_company.route('/add_partner', methods=["POST"])
def addPartner():
    partner_name = request.form.get("partner_name")
    partner_share = request.form.get("partner_share")

    if len(partner_name) < 1:
        flash("Partneri nimi peab olema täidetud", category="error")
    
    if partner_share < 1:
        flash("Partneri osa peab olema vähemalt 1€", category="error")
    
    return



