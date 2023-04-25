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


