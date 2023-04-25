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

function addPartner(){
    // add real logic to add partner
    let partner_name = $("#add-partner").val()
    let partner_share = $("#add-partner").val()
    if (!partner_name) {
        console.log("partner name can not be emty")
        return
    }
    $("#added-partners").append(`<div id='${partner_name}'>${partner_name}</div>`)
    $("#add-partner").val("")

    console.log("Partner added")
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