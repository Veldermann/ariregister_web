function searchAvaleht(){
    // API call for dynamic company search result
    $.ajax('/search', {
        type: 'POST',
        data: {"search": $("#search-company").val(),
               "search-by": $("#search-by").val()
        },
        success: function (data) {
            $('.search-result').html("");
            data.forEach(element => {
                let company_id = element['id']
                let registration_code = element['registration_code'];
                let company_name = element['name'];
                $('.search-result').append(`
                    <div id="${company_id}" class="company row" onclick="goCompanyView(this)">
                        <div class="company-registration-code col-6">${registration_code}</div>
                        <div class="company-name col-6">${company_name}</div>
                    </div>
                `);
            });
        }
    })
}

function goCompanyView(element){
    window.location.replace("/company?id=" + $(element).attr('id'));
}

// Top message handler
class AlertMessageHanlder {
    constructor(messages) {
        $(".current-message").remove()
        $('<div class="current-message"></div>').insertAfter('nav')
        if (messages.error && messages.error.length > 0) {
            for (const [key, value] of Object.entries(messages.error)){
                this.showError(value);
            }
        }

        if (messages.success.length > 0) {
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
function addShareholder(element) {
    let id = $(element).closest('.list-item').attr('data-id');
    let code = $(element).closest('.list-item').attr('id');
    let name = $(element).closest('.list-item').find('.name').html();
    let search_by = $('#shareholder-search-by').val();
    let checked = false;
    if (search_by == 'company_name' || search_by == 'registration_code') {
        checked = true;
    }
    if ($('#added-shareholders').children().length == 1){
        $("#added-shareholders").css('display', 'block');
    }

    let html = `
        <div id="${code}" class="row added-shareholder" data-id="${id}">
            <div class="col-3">
                <input type="text" name="shareholder-code" id="shareholder-code" class="form-control" value="${code}" disabled />
            </div>
            <div class="col-4">
                <input type="text" name="shareholder-name" id="shareholder-name" class="form-control" value="${name}" disabled />
            </div>
            <div class="col-3">
                <input type="number" name="share-size" id="share-size" class="form-control" value="0" />
            </div>
            <div class="col-1 btn-add-company">`;

    if (checked) {
        html += `<input type="checkbox" class="form-control" id="is-company" name="is-company" placeholder="Juuriidiline isik" checked disabled/>`;
    } else {
        html += `<input type="checkbox" class="form-control" id="is-company" name="is-company" placeholder="Juuriidiline isik" disabled/>`;
    }

    html += `
            </div>
            <div class="col-1 btn-add-company">
                <a name="remove" class="btn-remove-shareholder btn btn-danger" onclick="removeShareholder(this)"><i class="fa-solid fa-trash"></i></a>
            </div>
        </div>`;
    $('#added-shareholders').append(html);
    $('.search-result-dropdown').html('');
    $('.search-result-dropdown').css('display', 'none');
    $('#search-person-company').val('');
}

function removeShareholder(element) {
    $(element).closest('.added-shareholder').remove();
    if ($('#added-shareholders').children().length == 1){
        $('#added-shareholders').css('display', 'none');
    }
    const alerts = new AlertMessageHanlder({"success": ["Osanik eemaldatud."]});
}

function saveCompany() {
    let company_name = $("#company-name").val();
    let registration_code = $("#registration-code").val();
    let date_established = $("#registration-date").val();
    let total_capital = parseInt($("#total-capital").val());

    shareholders = []
    $('#added-shareholders').children().each(function() {
        if ($(this).hasClass('added-shareholders-header')){
            return;
        }
        let shareholder_id = $(this).attr('data-id');
        let share_size = parseInt($(this).find('#share-size').val());
        let is_company = $(this).find('#is-company').is(':checked');
        shareholders.push({'shareholder_id': shareholder_id, 'share_size': share_size, 'is_company': is_company});
    });
    var data = {"company_name": company_name, "registration_code": registration_code, "total_capital": total_capital, "date_established": date_established, "shareholders": shareholders};
    $.ajax("/add_company", {
        type: "POST",
        data: data,
        success: function(data) {
            const alerts = new AlertMessageHanlder(data);
            if (data.success.length){
                window.location.href = `/company?id${data.company_id}` ;
            }
        }
    })
}

$(document).ready(function(){
    // Set date max @ add_company page
    let current_url = window.location.pathname;
    if (current_url == '/add_company/') {
        let current_date = new Date();
        let current_year = current_date.getFullYear();
        let current_month = current_date.getMonth() + 1;

        if (current_month + 1 < 10) {
            current_month = "0" + current_month;
        }
        let current_day = current_date.getDate();
        $("#registration-date").attr("max", current_year + "-" + current_month + "-" + current_day);
    }
});

function searchPersonCompany(){
    // API call for dynamic person/company search result
    $.ajax('/add_company/search_person_company', {
        type: 'POST',
        data: {"search_string": $("#search-person-company").val(),
               "search_by": $("#shareholder-search-by").val()
        },
        success: function (data) {
            $('.search-result-dropdown').html("");
            if (data.length > 0) {
                $('.search-result-dropdown').css('display', 'block');
                data.forEach(element => {
                    let id = element[0]
                    let code = element[1];
                    let name = element[2];
                    $('.search-result-dropdown').append(`
                        <div id="${code}" class="list-item row" data-id="${id}">
                            <div class="col-5 code">${code}</div>
                            <div class="col-5 name">${name}</div>
                            <div class="col-2">
                                <a class="btn btn-primary" onclick="addShareholder(this)">+</i></a>
                            </div>
                        </div>
                    `);
                });
            } else {
                $('.search-result-dropdown').css('display', 'none');
            }
        }
    })
}