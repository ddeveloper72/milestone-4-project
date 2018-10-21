//waits until page is loaded first
$(document).ready(function () {
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
$('.timepicker').pickatime({
    default: 'now',
    twelvehour: false, // change to 12 hour AM/PM clock from 24 hour
    close: 'OK',
    autoclose: false,
    vibrate: true // vibrate the device when dragging clock hand
});

// select currently active depatrmtnt
$("#department").change(function() {
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
                optionToFill.append(`<option value="${element}" class="dept">${element}</option>`);
            });
        }
    });    
});

