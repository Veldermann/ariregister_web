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
        $(".current-message").remove()
        $('<div class="current-message"></div>').insertAfter('nav')
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
        $(".current-message").append(`
        <div class="alert alert-danger alter-dismissable fade show" role="alert">
            ${message}
            <button type="button" class="close">
                <span aria-hidden="true">×</span>
            </button>
        </div>`).delay(7000).fadeOut(1000, function() {
            $(this).remove();
        });
        this.addClose();
    }

    showSuccess(message) {
        $(".current-message").append(`
        <div class="alert alert-success alter-dismissable fade show" role="alert">
            ${message}
            <button type="button" class="close">
                <span aria-hidden="true">×</span>
            </button>
        </div>`).delay(7000).fadeOut(1000, function() {
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
    let total_capital = parseInt($("#total-capital").val());
    let registration_date = $("#registration-date").val();

    partners = []
    $('#added-partners').children().each(function() {
        let partner_name = $(this).find('#partner-name').val();
        let partner_share = parseInt($(this).find('#partner-share').val());
        partners.push({"partner_name": partner_name, "partner_share": partner_share});
    });
    var data = {"company_name": company_name, "registration_code": registration_code, "total_capital": total_capital, "registration_date": registration_date, "partners": partners};
    $.ajax("/add_company", {
        type: "POST",
        data: data,
        success: function(data) {
            const alerts = new alertMessage(data)
        }
    })
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