from flask import Blueprint, render_template, request, flash, redirect
from .validate.form_validator import FormValidator
from .save_company import saveCompany

add_company = Blueprint('add_company', __name__)

@add_company.route('/', methods=["GET", "POST"])
def main():
    if request.method == "POST":
        data = formControll(request)
        return data
        
    return render_template('add_company/add_company.html')

def formControll(data):
    validate_form = FormValidator(data)
    messages = validate_form.validate()
    if not messages['error']:
        company_id = saveCompany(validate_form.validatedData())
        return {'success': ['Ettevõte edukalt lisatud.'], 'company_id': company_id}

    return messages

