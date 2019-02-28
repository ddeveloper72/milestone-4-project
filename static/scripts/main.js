/* Service select script that generates a list dependent on the department selected              */
$("#departments").change(function() {
    let cur_value = $('option:selected' , this).val();
    console.log(cur_value);
    $.ajax({
        data: {
            dept_name : cur_value
        },        

        type: 'POST', // to python @app.route
        url: window.location.href.indexOf("edit") !== -1 ? "/service_update" :  "service"
    })
    .done((data) => {
        if (data.error) {
            console.log(data.error);
        } else {
            console.log(data);
            let optionToFill = $("#service");
            optionToFill.find('option').remove().end();
            data.data.forEach(function (element) {
                console.log(element);
                optionToFill.append(`<option value="${element}" class="dept">${element}</option>`);
            });
        }
    });    
});

/* Image select script used in add_department.html                                              */
/* Re-using function to select an image that relates to the department being selected           */
/* Using the same function to also inject a hdden input field that takes the actual image url   */
/* that can be retrieved for for the purpose of adding to the depatment document.               */
$("#add_department").change(function() {
    let cur_value = $('option:selected', this).val();
    console.log(cur_value);
    $.ajax({
        data: {
            dept_name : cur_value
        },        

        type: 'POST', // to python @app.route
        url: "/deptimg_update" 
    })
    .done((data) => {
        if (data.error) {
            console.log(data.error);
        } else {
            console.log(data);
            let optionToFill  = $("#dept_img");
            optionToFill.find('img').remove().end();
            data.data.forEach(function (element) {
            optionToFill.replaceWith(`<div class="img" id="dept_img" name="dept_img"> 
            <img class="card-img-top" name="dept_img" src="${element}" alt="Department Image">
            <input id="dept_img" type="hidden" name="img_url" value="${element}"></input>
            /div>`);
           
                
        });
    }
});    
});

/* Services select script used in add_department.html                                            */
$("#add_department").change(function() {
    let cur_value = $('option:selected', this).val();
    console.log(cur_value);
    $.ajax({
        data: {
            dept_name : cur_value
        },        

        type: 'POST', // to python @app.route
        url: "/dept_update" 
    })
    .done((data) => {
        if (data.error) {
            console.log(data.error);
        } else {
            console.log(data);
            let input  = $("#list_service");
            input.find('li').remove().end();
            data.data.forEach(function (element) {
                console.log(element);
                input.append(`<li><input class="form-check-input" id="list_service" name="service" type="checkbox" value="${element}" unchecked>${element}</input></li>`);
                
                
            });
        }
    });    
});


/* Services select script used in add_appointment.html                                           */
var selected = [];
$('#list_service input:checked').each(function() {
    selected.push($(this).attr('name'));
    return this.name;
});

/* Datetime picker config script. Time increments in 15min intervals                             */
$(function () {
    $('#datetimepicker').datetimepicker({
        icons: {
            time: 'far fa-clock',
            date: 'far fa-calendar-alt',
            up: 'fas fa-arrow-up',
            down: 'fas fa-arrow-down',
            previous: 'fas fa-chevron-left',
            next: 'fas fa-chevron-right',
            today: 'far fa-calendar-check',
            clear: 'fas fa-trash',
            close: 'fas fa-times'
        },
        locale: 'en-ie',
		allowInputToggle: true,
		minDate: moment(),
		stepping: 15,
		showClose: true
    });
});

/* Confirm deletion prompt                                                                       */
$(document).on('click', '.confirm-delete', function(){
    return confirm('Are you sure you want to delete this?');
});

/* Add toolips for descriptive user infomation                                                    */
$(function () {
    $('[data-toggle="tooltip"]').tooltip()
  });

/* jQuery Mask Plugin adapted from Igor Escobar https://igorescobar.github.io/jQuery-Mask-Plugin/ */
  $(document).ready(function(){
    $('.phone_with_ddd').mask('(000) 000-0000');
  });