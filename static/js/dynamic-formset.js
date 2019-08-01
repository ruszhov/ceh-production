function cloneMore(selector, type) {
    var $orginal = $(selector);
    var newElement = $(selector).clone(true);
    var total_forms = $('#id_form-TOTAL_FORMS').val();
    // console.log(total_forms);
    
    newElement.find(':input').each(function() {
        var this_name = $(this).attr('name');
        // console.log(this_name);
        var name = $(this).attr('name').replace('-' + (total_forms-1) + '-','-' + total_forms + '-');
        //console.log(name);
        var id = 'id_' + name;
        // console.log(id);
        $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');

    });
    newElement.find('label').each(function() {
        var newFor = $(this).attr('for').replace('-' + (total_forms-1) + '-','-' + total_forms + '-');
        // console.log(newFor);
        $(this).attr('for', newFor);
    });

    total_forms++;
    // console.log(total_forms);
    $('#id_form-TOTAL_FORMS').val(total_forms);
    $(selector).after(newElement);

}

//клонування форми для нового рахунку
function cloneMaterialorder(selector, type) {
    var $orginal = $(selector);
    var newElement = $(selector).clone();
    var total_forms = $('#id_form-TOTAL_FORMS').val();
    // console.log(total_forms);

    var total_forms = $('#id_form-TOTAL_FORMS').val();
    // console.log(total_forms);
    
    newElement.find(':input').each(function() {
        var this_name = $(this).attr('name');
        // console.log(this_name);
        var name = $(this).attr('name').replace('-' + (total_forms-1) + '-','-' + total_forms + '-');
        //console.log(name);
        var id = 'id_' + name;
        // console.log(id);
        $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');

    });

    //навігація для табів
    newElement.find('div.nav a').each(function(){
        var this_id = $(this).attr('href');
        // console.log(this_id);
        var new_id = $(this).attr('href').replace('-' + (total_forms-1) + '-','-' + total_forms + '-');
        // console.log(new_id);
        $(this).attr('href', new_id);
    })

    //таби
    newElement.find('div.tab-pane').each(function(){
        var pane_id = $(this).attr('id');
        // console.log(pane_id);
        var new_pane_id = $(this).attr('id').replace('-' + (total_forms-1) + '-','-' + total_forms + '-');
        // console.log(new_pane_id);
        $(this).attr('id', new_pane_id);
    })

    //кнопка видалити
    var span = newElement.find('#del_current_order svg').removeClass( "hidden" );

    // console.log(span);

    newElement.find('#del_current_order').on('click', function(){
        $(this).closest('div.selector-to-clone').fadeOut(300, function(){
            var remove = $(this).remove();
            var total_forms = $('#id_form-TOTAL_FORMS').val();
            $('#id_form-TOTAL_FORMS').val(total_forms - 1);
        });
    })

    total_forms++;
    // console.log(total_forms);
    $('#id_form-TOTAL_FORMS').val(total_forms);
    $(selector).after(newElement);

    // newElement.find("select[name$='material']").each(function(){
    // var selectedValue = this.selectedOptions[0].value;
    // var selectedText  = this.selectedOptions[0].text;
    // console.log(selectedValue);
    // })

}


