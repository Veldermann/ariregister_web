function search(element){
    // console.log(element.value)
    // API call for dynamic company search result
    $.ajax('/search', {
        type: 'POST',
        data: {"search": element.value},
        success: function (data) {
            console.log(data)
        }
    })
}

// Top message handler
class alertMessage {
    constructor(messages) {
        if (messages.error && messages.error.length > 0) {
            console.log(messages.error)
            for (const [key, value] of Object.entries(messages.error)){
                this.showError(value);
            }
        }

        if (messages.success.length > 0) {
            console.log(messages.success)
            for (const [key, value] of Object.entries(messages.success)){
                this.showSuccess(value);
            }
        }
    }

    showError(message) {
        $(`<div class="alert alert-danger alter-dismissable fade show" role="alert">
                ${message}
                <button type="button" class="close">
                    <span aria-hidden="true">×</span>
                </button>
        </div>`).insertAfter('nav').delay(7000).fadeOut(1000, function() {
            $(this).remove();
        });
        this.addClose();
    }

    showSuccess(message) {
        $(`<div class="alert alert-success alter-dismissable fade show" role="alert">
            ${message}
            <button type="button" class="close">
                <span aria-hidden="true">×</span>
            </button>
        </div>`).insertAfter('nav').delay(7000).fadeOut(1000, function() {
            $(this).remove();
        });
        this.addClose();
    }

    addClose() {
        $(".close").on("click", function() {
            $(this).parent().remove();
        });
    }
}

function addPartner(){
    let partner_name = $("#add-partner-name").val()
    let partner_share = parseInt($("#add-partner-share").val())
    let total_capital = $("#total-capital").val()

    let total_partners_share = 0
    $("#added-partners").children().each(function() {
        total_partners_share += parseInt($(this).find('#partner-share').val())
    })
    total_partners_share += partner_share
    console.log(total_partners_share);
    $.ajax('/add_company/add_partner', {
        type: 'POST',
        data: {'partner_name': partner_name,
               'partner_share': partner_share,
               'total_capital': total_capital,
               'total_partners_share': total_partners_share
            },
        success: function (data) {
            const alerts = new alertMessage(data)
            if (data.success.length > 0) {
                $("#added-partners").append(`<div id="${partner_name}" class="row added-partner">
                                                <div class="col-7">
                                                    <input type="text" id="partner-name" class="form-control" value="${partner_name}" disabled />
                                                </div>
                                                <div class="col-3">
                                                    <input type="number" id="partner-share" class="form-control" value="${partner_share}" disabled />
                                                </div>
                                                <div class="col-1">
                                                    <a class="btn-edit-save-partner btn btn-secondary" onclick="editSavePartnerBtn(this)"><i class="fa-solid fa-pencil"></i></a>
                                                </div>
                                                <div class="col-1">
                                                    <a class="btn-remove-partner btn btn-danger" onclick="removePartner(this)"><i class="fa-solid fa-trash"></i></a>
                                                </div>
                                            </div>`);
                $("#add-partner-name").val("");
                $("#add-partner-share").val("");
            }
        }
    })
}

function removePartner(element) {
    $(element).parent().parent().remove();
    const alerts = new alertMessage({"success": ["Partner eemaldatud."]});
}

function editSavePartnerBtn(element) {
    if ($(element).parent().parent().find('#partner-share').is(':disabled')) {
        $(element).parent().parent().find('#partner-share').prop('disabled', false);
        $(element).html(`<i class="fas fa-save"></i>`)
    } else {
        $(element).parent().parent().find('#partner-share').prop('disabled', true);
        $(element).html('<i class="fa-solid fa-pencil"></i>') 
    }
}

function saveCompany() {
    let company_name = $("#company-name").val();
    let registration_code = $("#registration-code").val();
    let total_capital = $("#total-capital").val();
    console.log(company_name);
    console.log(registration_code);
    console.log(total_capital);
    let partners = [];
    $('#added-partners').children().each(function() {
        partners.push([$(this).find('#partner-name').val(), $(this).find('#partner-share').val()]);
    })
    console.log(partners);
}

$(document).ready(function(){
    let current_date = new Date()
    let current_year = current_date.getFullYear()
    let current_month = current_date.getMonth() + 1

    if (current_month + 1 < 10) {
        current_month = "0" + current_month
    }
    let current_day = current_date.getDate()
    $("#registration-date").attr("max", current_year + "-" + current_month + "-" + current_day)
})