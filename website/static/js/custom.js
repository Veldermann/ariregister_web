function search(element){
    // 8console.log(element.value)
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
    constructor(message) {
        if (message.error) {
            for (const [key, value] of Object.entries(message.error)){
                this.showError(value);
            }
        }

        if (message.success) {
            for (const [key, value] of Object.entries(message.success)){
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
        </div>`).insertAfter('nav').delay(7000).fadeOut(1000);
        this.addClose();
    }

    showSuccess(message) {
        $(`<div class="alert alert-success alter-dismissable fade show" role="alert">
            ${message}
            <button type="button" class="close" data-dismiss="alert">
                <span aria-hidden="true">×</span>
            </button>
        </div>`).insertAfter('nav').delay(7000).fadeOut(1000);
        this.addClose();
    }

    addClose() {
        $(".close").on("click", function() {
            console.log("Close clicked");
            $(this).parent().hide();
        });
    }
}

function addPartner(){
    let partner_name = $("#add-partner-name").val()
    let partner_share = $("#add-partner-share").val()

    $.ajax('/add_company/add_partner', {
        type: 'POST',
        data: {'partner_name': partner_name,
               'partner_share': partner_share
            },
        success: function (data) {
            const alerts = new alertMessage(data)
            $("#added-partners").append(`<div id='${partner_name}'>${partner_name}</div>`)
            $("#add-partner").val("")
        }
    })
}

$(document).ready(function(){
    let current_date = new Date()
    let current_year = current_date.getFullYear()
    let current_month = current_date.getMonth() + 1
    if (current_month + 1 < 10) {
        current_month = "0" + current_date.getMonth()
    }
    let current_day = current_date.getDate()
    $("#registration-date").attr("max", current_year + "-" + current_month + "-" + current_day)
})