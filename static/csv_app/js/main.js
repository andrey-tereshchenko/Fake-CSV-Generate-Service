$(document).ready(function () {
    var maxField = 10; //Input fields increment limitation
    var addButton = $('.add_button'); //Add button selector
    var wrapper = $('.field_wrapper'); //Input field wrapper
    var fieldHTML = '<div class="form-row">\n' +
        '                <div class="form-group col-md-3">\n' +
        '                    <label for="inputColumnName">Column Name</label>\n' +
        '                    <input name="column_name[]" type="text" class="form-control" id="inputColumnName">\n' +
        '                </div>\n' +
        '                <div class="form-group col-md-3">\n' +
        '                    <label for="inputType">Type</label>\n' +
        '                    <select name="column_type[]" id="inputType" class="form-control">\n' +
        '                        <option selected>-------</option>\n' +
        '                        <option>Full name</option>\n' +
        '                        <option>Job</option>\n' +
        '                        <option>Email</option>\n' +
        '                        <option>Domain</option>\n' +
        '                        <option>Phone number</option>\n' +
        '                        <option>Company</option>\n' +
        '                        <option value="txt">Text</option>\n' +
        '                        <option value="int">Integer</option>\n' +
        '                        <option>Address</option>\n' +
        '                        <option>Date</option>\n' +
        '                    </select>\n' +
        '                </div>\n' +
        '                <div class="form-group col-md-1" style="visibility: hidden;">\n' +
        '                    <label for="inputFrom">From</label>\n' +
        '                    <input name="from[]" type="text" class="form-control" id="inputFrom">\n' +
        '                </div>\n' +
        '                <div class="form-group col-md-1" style="visibility: hidden;">\n' +
        '                    <label for="inputTo">To</label>\n' +
        '                    <input name="to[]" type="text" class="form-control" id="inputTo">\n' +
        '                </div>\n' +
        '                <div class="form-group col-md-2">\n' +
        '                    <label for="inputOrder">Order</label>\n' +
        '                    <input name="order[]" type="text" class="form-control" id="inputOrder">\n' +
        '                </div>\n' +
        '<div class="form-group col-md-1" style="margin: auto"><a href="javascript:void(0);" class="remove_button btn">Remove</a></div>' +
        '            </div>'; //New input field html
    var x = 1; //Initial field counter is 1

    //Once add button is clicked
    $(addButton).click(function () {
        //Check maximum number of input fields
        if (x < maxField) {
            x++; //Increment field counter
            $(wrapper).prepend(fieldHTML); //Add field html
        }
    });

    //Once remove button is clicked
    $(wrapper).on('click', '.remove_button', function (e) {
        e.preventDefault();
        $(this).parent('div').parent('div').remove(); //Remove field html
        x--; //Decrement field counter
    });
// '#div_id_column_set-0-order'
    $('table').on('change', "div:regex(id, div_id_column_set-*-order)", function(){
        var sel = $(this).val();
        if (sel == 'int' || sel == 'txt') {
            $(this).parent('div').next('div').css('visibility', 'visible');
            $(this).parent('div').next('div').next('div').css('visibility', 'visible');
        }
        else {
            $(this).parent('div').next('div').css('visibility', 'hidden');
            $(this).parent('div').next('div').next('div').css('visibility', 'hidden');
        }
    });
});