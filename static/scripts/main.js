//waits until page is loaded first
$(document).ready(function () {
    Materialize.updateTextFields();
    $('.collapsible').collapsible();
    $('select').material_select();
    $('.button-collapse').sideNav();
    $('.datepicker').pickadate();
    $('.timepicker').pickatime();
});

// Date picker:
$('.datepicker').pickadate({
    selectMonths: true, // Creates a dropdown to control month
    selectYears: 15, // Creates a dropdown of 15 years to control year,
    today: 'Today',
    clear: 'Clear',
    close: 'Ok',
    closeOnSelect: false // Close upon selecting a date,
});

// Credit to https://github.com/chingyawhao/materialize-clockpicker/
// Time picker:
$("#departments").change(function() {
    let cur_value = $('option:selected', this).val();
    console.log(cur_value);
    $.ajax({
        data: {
            ref : cur_value
        },
        type: 'POST',
        url: '/services'
    })
    .done((data) => {
        if (data.error) {
            console.log(data.error)
        } else {
            console.log(data);
            let optionToFill = $("#services");
            optionToFill.find("option").remove().end();
            data.data.forEach((element) => {
                optionToFill
                .append(`<option value="${element}">${element}</option>`);
            });
        }
    });    
});


// Secondary TEST jQuery function
/* $("#departments").change(function() {
    let cur_value = $('option:selected', this).val();
    console.log(cur_value);
    $.ajax({
        data: {
            ref : cur_value
        },
        type: 'POST',
        url: '/services'
    })
    .done((data) => {
        if (data.error) {
            console.log(data.error)
        } else {
            console.log(data);
            let optionToFill = $("#services");
            optionToFill.find('option').remove().end();
            data.data.forEach((element) => {
                $("ul").last().append(`<li class="bob"><span>${element}</span></li>`)
                    optionToFill.append(`<option value="${element}" class="dept">${element}</option>`);
            });
            $(".bob").click(function() {
                $(this).removeClass("bob").addClass("active").addClass("selected");
            });
        }
    });    
}); */

