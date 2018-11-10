// select currently active department & return the data to python @app.route

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
            console.log(data.error)
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
            console.log(data.error)
        } else {
            console.log(data);
            let input  = $("#list_service");
            input.find('li').remove().end();
            data.data.forEach(function (element) {
                console.log(element);
                input.append(`<li><input class="form-check-input" id="service" name="service" type="checkbox" value="${element}" unchecked>${element}</input></li>`)
                
                
            });
        }
    });    
});

$(function () {
    $('#datetimepicker2').datetimepicker({ 
        bootstricons: {
            time: "far fa-clock",
            date: "far fa-calendar",
            up: "fas fa-arrow-up",
            down: "fas fa-arrow-down"
        }
    });
});