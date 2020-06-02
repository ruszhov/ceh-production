function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

setInterval(function() {
    $("td.t11").each(function(){
    if($(this).is(':contains("Виконано")')) {
    }
    else
    {
        var data = {};
        data["csrfmiddlewaretoken"]= getCookie('csrftoken');
        data["order_id"]=this.dataset.orderId;
        data["status"]=this.textContent;
        // console.log(this.textContent);
        // console.log(data);
        $.ajax({
            url : 'check_print_status/',
            type : "POST",
            data : data,
            cache: false,
            success: function(response){
               if(response == 'False'){}
               else {
                   var response_status = response.status;
                   var response_product_id = response.product_id;

                   if(response.user.username != 'not_user'){
                       var response_user = response.user.username;
                   };
                   var target = $('td.t11[data-order-id=' + response_product_id + ']');
                   var target_content = target.text().trim();
                   if(response_status != target_content){

                       if(response_status == 'Виконано'){
                           var n = target.html("<span> "+response_status+"</span>");
                           target.find('span').css('padding-left', '15px');
                           var user_target = target.closest('tr').find('td.t12').html(response_user);
                           var statusOleg  = $("#main-table td.t12:contains('Олег')").closest('tr').find("td:contains('Виконано')").addClass('table-success');
                           var statusPetro = $("#main-table td.t12:contains('Петро')").closest('tr').find("td:contains('Виконано')").addClass('table-warning');
                           var statusSerg  = $("#main-table td.t12:contains('Сергій')").closest('tr').find("td:contains('Виконано')").addClass('table-danger');
                           // var statusRoman  = $("#main-table td.t12:contains('Роман'), #main-table td.t12:contains('Остап')").closest('tr').find("td:contains('Виконано')").css('background-color', '#FFB775');
                       }
                       else {
                           var currentLocation = window.location.origin;
                           var full_edit_url = currentLocation + '/status/' + response_product_id + '/edit/?next=/';
                           var n = target.html(response_status);
                           n.prepend("<a href='" + full_edit_url + "'><i class=\"fas fa-pencil-alt\"></i></a> ");
                           target.find('a').css('color', 'rgb(255, 165, 0)');
                       }
                   }
               }
            }
        })
    }
});
}, 60000);
