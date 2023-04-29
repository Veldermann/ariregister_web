function searchAvaleht(){
    // API call for dynamic company search result
    $.ajax('/search', {
        type: 'POST',
        data: {"search": $("#search-company").val(),
               "search-by": $("#search-by").val()
        },
        success: function (data) {
            console.log(data)
            $('.search-result').html("");
            data.forEach(element => {
                registration_code = Object.keys(element);
                company_name = element[registration_code];
                $('.search-result').append(`
                    <div id="${registration_code}" class="company row" onclick="goCompanyView(this)">
                        <div class="company-registration-code col-6">${registration_code}</div>
                        <div class="company-name col-6">${company_name}</div>
                    </div>
                `);
            // Make search results clickable
            });
        }
    })
}

function goCompanyView(element){
    window.location.replace("/company?registration_code=" + $(element).attr('id'));
}

function changeShareholderCompany(){
    if ($("#is-company").is(":checked")){
        $(".add-shareholder-content").html(`
        <div class="form-group row">
            <label for="add-shareholder-name" class="col-4">Ettevõtte nimi</label>
            <label for="add-shareholder-code" class="col-4">Registrikood</label>
            <label for="add-share-size" class="col-2">Osa suurus</label>
            <label for="is-company" class="col-1">Juuriidiline- isik</label>
        </div>
        <div class="form-group row">
            <div class="col-4">
                <input type="text" class="form-control" id="add-shareholder-name" name="add-shareholder-name" placehodler="Lisa osaniku nimi" />
            </div>
            <div class="col-4">
                <input type="text" class="form-control" id="add-shareholder-code" name="add-shareholder-code" placehodler="Lisa osaniku isikukood" />
            </div>
            <div class="col-2">
                <input type="number" class="form-control" id="add-share-size" name="add-share-size" placehodler="Osaniku osa suurus" value="0" />
            </div>
            <div class="col-1 btn-add-company">
                <input type="checkbox" class="form-control" id="is-company" name="is-company" placeholder="Juuriidilineisik" onchange="changeShareholderCompany()" checked/>
            </div>
            <div class="col-1 btn-add-company">
                <a id="btn-add-shareholder" class="btn btn-primary" onclick="addShareholder()"><i class="fa-solid fa-plus"></i></a>
            </div>
        </div>
        `)
    } else {
        $(".add-shareholder-content").html(`
            <div class="form-group row">
                <label for="add-shareholder-name" class="col-2">Eesnimi</label>
                <label for="add-shareholder-name" class="col-3">Perekonnanimi</label>
                <label for="add-shareholder-code" class="col-3">Isikukood</label>
                <label for="add-share-size" class="col-2">Osa suurus</label>
                <label for="is-company" class="col-1">Juuriidiline- isik</label>
            </div>
            <div class="form-group row">
                <div class="col-2">
                    <input type="text" class="form-control" id="add-shareholder-name" name="add-shareholder-name" placehodler="Lisa osaniku nimi" />
                </div>
                <div class="col-3">
                    <input type="text" class="form-control" id="add-shareholder-lastname" name="add-shareholder-lastname" placehodler="Lisa osaniku perekonnanimi" />
                </div>
                <div class="col-3">
                    <input type="text" class="form-control" id="add-shareholder-code" name="add-shareholder-code" placehodler="Lisa osaniku isikukood" />
                </div>
                <div class="col-2">
                    <input type="number" class="form-control" id="add-share-size" name="add-share-size" placehodler="Osaniku osa suurus" value="0" />
                </div>
                <div class="col-1 btn-add-company">
                    <input type="checkbox" class="form-control" id="is-company" name="is-company" placeholder="Juuriidilineisik" onchange="changeShareholderCompany()"/>
                </div>
                <div class="col-1 btn-add-company">
                    <a id="btn-add-shareholder" class="btn btn-primary" onclick="addShareholder()"><i class="fa-solid fa-plus"></i></a>
                </div>
            </div>
        `)
    }
    return
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

function addShareholder(){
    let shareholder_name = $("#add-shareholder-name").val()
    let shareholder_lastname = $("#add-shareholder-lastname").val()
    let shareholder_code = $("#add-shareholder-code").val()
    let share_size = parseInt($("#add-share-size").val())
    let is_company = $("#is-company").is(":checked")
    let total_capital = $("#total-capital").val()

    let total_shareholders_share = 0
    $("#added-shareholders").children().each(function() {
        total_shareholders_share += parseInt($(this).find('#share-size').val())
    })
    total_shareholders_share += share_size

    $.ajax('/add_company/add_shareholder', {
        type: 'POST',
        data: {'shareholder_name': shareholder_name,
               'sharehodler_lastname': shareholder_lastname,
               'shareholder_code': shareholder_code,
               'share_size': share_size,
               'is_company': is_company,
               'total_capital': total_capital,
               'total_shareholders_share': total_shareholders_share
            },
        success: function (data) {
            const alerts = new AlertMessageHanlder(data)
            if (data.success.length > 0) {
                if (is_company && !$('#added-shareholders .added-companies').hasClass('added-companies')){
                    $("#added-shareholders").append(`
                        <div class="added-companies">
                            <div class="form-group row">
                                <label for="shareholder-name" class="col-4">Ettevõtte nimi</label>
                                <label for="shareholder-code" class="col-4">Registrikood</label>
                                <label for="share-size" class="col-2">Osa suurus</label>
                                <label for="edit" class="col-1">Muuda</label>
                                <label for="remove" class="col-1">Kustuta</label>
                            </div>
                        </div>
                    `);
                } 
                if (!is_company && !$('#added-shareholders .added-shareholders').hasClass('added-shareholders')) {
                    $("#added-shareholders").append(`
                    <div class="added-shareholders">
                        <div class="form-group row">
                            <label for="shareholder-name" class="col-2">Eesnimi</label>
                            <label for="shareholder-lastname" class="col-3">Perekonnanimi</label>
                            <label for="shareholder-code" class="col-3">Isikukood</label>
                            <label for="share-size" class="col-2">Osa suurus</label>
                            <label for="edit" class="col-1">Muuda</label>
                            <label for="delete" class="col-1">Kustuta</label>
                        </div>
                    </div>
                `);

                }

                if (!is_company) {
                    $("#added-shareholders .added-shareholders").append(`
                        <div id="${shareholder_name}" class="row added-shareholder">
                            <div class="col-2">
                                <input type="text" name="shareholder-name" id="shareholder-name" class="form-control" value="${shareholder_name}" disabled />
                            </div>
                            <div class="col-3">
                                <input type="text" name="shareholder-lastname" id="shareholder-lastname" class="form-control" value="${shareholder_lastname}" disabled />
                            </div>
                            <div class="col-3">
                                <input type="text" name="shareholder-code" id="shareholder-code" class="form-control" value="${shareholder_code}" disabled />
                            </div>
                            <div class="col-2">
                                <input type="number" name="share-size" id="share-size" class="form-control" value="${share_size}" disabled />
                            </div>
                            <div class="col-1 btn-add-company">
                                <a name="edit" class="btn-edit-save-shareholder btn btn-secondary" onclick="editSaveShareholderBtn(this)"><i class="fa-solid fa-pencil"></i></a>
                            </div>
                            <div class="col-1 btn-add-company">
                                <a name="remove" class="btn-remove-shareholder btn btn-danger" onclick="removeShareholder(this)"><i class="fa-solid fa-trash"></i></a>
                            </div>
                        </div>
                    `);
                } else {
                    $("#added-shareholders .added-companies").append(`
                        <div id="${shareholder_name}" class="row added-shareholder">
                            <div class="col-4">
                                <input type="text" name="shareholder-name" id="shareholder-name" class="form-control" value="${shareholder_name}" disabled />
                            </div>
                            <div class="col-4">
                                <input type="text" name="shareholder-code" id="shareholder-code" class="form-control" value="${shareholder_code}" disabled />
                            </div>
                            <div class="col-2">
                                <input type="number" name="share-size" id="share-size" class="form-control" value="${share_size}" disabled />
                            </div>
                            <div class="col-1 btn-add-company">
                                <a name="edit" class="btn-edit-save-shareholder btn btn-secondary" onclick="editSaveShareholderBtn(this)"><i class="fa-solid fa-pencil"></i></a>
                            </div>
                            <div class="col-1 btn-add-company">
                                <a name="remove" class="btn-remove-shareholder btn btn-danger" onclick="removeShareholder(this)"><i class="fa-solid fa-trash"></i></a>
                            </div>
                        </div>
                    `);       
                }
                $("#add-shareholder-name").val("");
                $("#add-shareholder-code").val("");
                $("#is_company").prop( "checked", false );
                $("#add-share-size").val("");
            }
        }
    })
}

function removeShareholder(element) {
    $(element).parent().parent().remove();
    if ($(element).closest('.added-shareholders').children().length < 1){
        $('.added-shareholders').remove();
    }
    const alerts = new AlertMessageHanlder({"success": ["Osanik eemaldatud."]});
}

function editSaveShareholderBtn(element) {
    if ($(element).parent().parent().find('#share-size').is(':disabled')) {
        $(element).parent().parent().find('#share-size').prop('disabled', false);
        $(element).html(`<i class="fas fa-save"></i>`)
    } else {
        $(element).parent().parent().find('#share-size').prop('disabled', true);
        $(element).html('<i class="fa-solid fa-pencil"></i>') 
    }
}

function saveCompany() {
    let company_name = $("#company-name").val();
    let registration_code = $("#registration-code").val();
    let total_capital = parseInt($("#total-capital").val());
    let registration_date = $("#registration-date").val();

    shareholders = []
    $('#added-shareholders').children().each(function() {
        let shareholder_name = $(this).find('#shareholder-name').val();
        let share_size = parseInt($(this).find('#share-size').val());
        shareholders.push({"shareholder_name": shareholder_name, "share_size": share_size});
    });
    var data = {"company_name": company_name, "registration_code": registration_code, "total_capital": total_capital, "registration_date": registration_date, "shareholders": shareholders};
    $.ajax("/add_company", {
        type: "POST",
        data: data,
        success: function(data) {
            const alerts = new AlertMessageHanlder(data)
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




