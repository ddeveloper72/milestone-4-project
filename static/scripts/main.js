// select currently active department
$("#departments").change(function() {
    let cur_value = $('option:selected', this).val();
    console.log(cur_value);
    $.ajax({
        data: {
            ref : cur_value
        },
        type: 'POST',
        url: '/service'
    })
    .done((data) => {
        if (data.error) {
            console.log(data.error)
        } else {
            console.log(data);
            let optionToFill = $("#service");
            optionToFill.find('option').remove().end();
            data.data.forEach((element) => {
                optionToFill.append(`<option value="${element}" class="dept">${element}</option>`);
            });
        }
    });    
});
