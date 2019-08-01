$(document).click(function(event) {
   window.lastElementClicked = event.target;
});

$(document).ready(function(){
	
	//проставляємо 1 в строці к-ть якщо там ще нічого не стоїть
	var startNumber = $("td.new_ord_nmb input[name$='number']");
	if ( startNumber.val() == '')
	{
		startNumber.val('1');
	}
	else
	{}
	// $('input, select, textarea').addClass('form-control');

	$('#new_order').find('input, select, textarea').addClass('form-control');
	$('.printorder-status').find('input, select, textarea').addClass('form-control');
	$('.new_campaign').find('input, select, textarea').addClass('form-control');
	$('.edit-printorder-description').find('input, select, textarea').addClass('form-control');

	$('#new_order').find('input, select').css({
		"width": "100%",
		"height": "28px",
		"padding": "3px 12px",
		"font-size": "12px",
	});

	$('#new_order').find('textarea').css({
		"width": "100%",
		"height": "50px",
		"padding": "3px 12px",
		"font-size": "12px",
	})

	// $("#id_form-0-print_height").on("change paste keyup", function() {
	//    alert($(this).val()); 
	// });

	$('td.formatka').find('a').css('color', 'white');
 
	//додавання значень для форматки і стилі кнопок
	$('#a0n').click(function(event){
		$(this).closest('table').find("input[name$='print_width']").val('0.841');
		$(this).closest('table').find("input[name$='print_height']").val('1.189');
	})
	$('#a1n').click(function(event){
		$(this).closest('table').find("input[name$='print_width']").val('0.594');
		$(this).closest('table').find("input[name$='print_height']").val('0.841');
	})
	$('#a2n').click(function(event){
		$(this).closest('table').find("input[name$='print_width']").val('0.42');
		$(this).closest('table').find("input[name$='print_height']").val('0.594');
	})
	$('#a3n').click(function(event){
		$(this).closest('table').find("input[name$='print_width']").val('0.297');
	    $(this).closest('table').find("input[name$='print_height']").val('0.42');
	});

	$('#a4n').click(function(event){
	    $(this).closest('table').find("input[name$='print_width']").val('0.21');
	    $(this).closest('table').find("input[name$='print_height']").val('0.297');
	});
	$('#a5n').click(function(event){
	    $(this).closest('table').find("input[name$='print_width']").val('0.148');
	    $(this).closest('table').find("input[name$='print_height']").val('0.21');
	});
	$('#a6n').click(function(event){
	    $(this).closest('table').find("input[name$='print_width']").val('0.105');
	    $(this).closest('table').find("input[name$='print_height']").val('0.148');
	});
	$('#andel').click(function(event){
		$(this).closest('table').find("input[name$='print_width']").val('');
	    $(this).closest('table').find("input[name$='print_height']").val('');
	    $(this).closest('table').find("input[name$='number']").val('1');
	    $(this).closest('table').find("input[name$='m_kv']").val('');
	    $(this).siblings().removeClass('btn-danger').addClass('btn-secondary');
	    $(this).closest('td').siblings().find('a.btn-danger').removeClass('btn-danger').addClass('btn-secondary');
 		$(this).closest('tr').siblings().find('a.btn-danger').removeClass('btn-danger').addClass('btn-secondary');
	});
	// постери
	$('#6x3').click(function(event){
	    $(this).closest('table').find("input[name$='print_width']").val('6');
	    $(this).closest('table').find("input[name$='print_height']").val('3');
	});
	$('#5_9x2_9').click(function(event){
	    $(this).closest('table').find("input[name$='print_width']").val('5.9');
	    $(this).closest('table').find("input[name$='print_height']").val('2.9');
	});
	$('#4x3').click(function(event){
	    $(this).closest('table').find("input[name$='print_width']").val('4');
	    $(this).closest('table').find("input[name$='print_height']").val('3');
	});
	//сітiк/скролл
	$('#3_14x2_32').click(function(event){
	    $(this).closest('table').find("input[name$='print_width']").val('3.14');
	    $(this).closest('table').find("input[name$='print_height']").val('2.32');
	});
	$('#3_14x2_3').click(function(event){
	    $(this).closest('table').find("input[name$='print_width']").val('3.14');
	    $(this).closest('table').find("input[name$='print_height']").val('2.3');
	});
	$('#1_2x1_8').click(function(event){
	    $(this).closest('table').find("input[name$='print_width']").val('1.8');
	    $(this).closest('table').find("input[name$='print_height']").val('1.2');
	});
	$('#1_27x1_86').click(function(event){
	    $(this).closest('table').find("input[name$='print_width']").val('1.86');
	    $(this).closest('table').find("input[name$='print_height']").val('1.27');
	});
	
	$('#add_more').click(function(event){

		//Берем значення select з попередньої таблиці
		var previous = $("div.container div.table:last").prev("div.table");
		var prevNameOfCamp = previous.find("select[name$='name_of_camp'] :selected").val();
		var prevMaterial = previous.find("select[name$='material'] :selected").val();
		var prevManager = previous.find("select[name$='manager'] :selected").val();
		var prevStatus = previous.find("select[name$='status'] :selected").val();
		var prevPrioritet = previous.find("select[name$='prioritet'] :selected").val();

		//Беремо значення ширини, висоти, кількості та площі з попередньої таблиці
		var prevHeight = previous.find("input[name$='height']").val();
		var prevWidth = previous.find("input[name$='width']").val();
		var prevNumb = previous.find("input[name$='number']").val();
		var prevMkv = previous.find("input[name$='m_kv']").val();

		//Копіюєм значення select, взяті перед тим в поточну талицю
		var current = $("div.container div.table:last");
		// var curnumber = current.find($("input[name$='number']").val('1'));
		var currentNameOfCamp = current.find("select[name$='name_of_camp']").val(prevNameOfCamp);
		var currentMaterial = current.find("select[name$='material']").val(prevMaterial);
		var currentManager = current.find("select[name$='manager']").val(prevManager);
		var currentStatus = current.find("select[name$='status']").val(prevStatus);
		var currentPrioritet = current.find("select[name$='prioritet']").val(prevPrioritet);
		
		//копіюєм значення ширини, висоти, кількості та площі з попередньої таблиці
		var curHeight = current.find("input[name$='height']").val(prevHeight);
		var curWidth = current.find("input[name$='width']").val(prevWidth);
		var curNumb = current.find("input[name$='number']").val(prevNumb);
		var curMkv = current.find("input[name$='m_kv']").val(prevMkv);
	});

	//Делегуємо новоствореній кнопці властивості
	$(".edit-buttons").on("click", "#del_last", function(event){
	    $("div.container div.table:last").remove();
	    var total_forms = $('#id_form-TOTAL_FORMS').val();
	    $('#id_form-TOTAL_FORMS').val(total_forms - 1);
	});

	$(".edit-buttons").on("click", "#del_last", function(event){
	    var n = $( ".container div.table" ).length;
	    if ( n <= 1) {
	    	$("button#del_last").remove();
	    }
	    else
	    {}
        // console.log(n);
	});

	//додаємо кнопку "Видалити останню"
	$( "#add_more" ).on( "click", function() {
	  var r= $('<button type="button" class="btn btn-danger" id="del_last">Видалити останнє замовлення</button>');
        $(".col-sm-3").append(r);
	});

	$( "#add_more" ).on( "click", function() {
		$("tr.last-row").css("border", "1px solid red");
	} );

	//скриваэмо кнопку
	$( "#add_more" ).on("click", function(){
		var len = $(" #del_last ").length;
		if (len > 1){
			$(".edit-buttons button#del_last:last").remove();
		}
	});

	//перемотка сторынки до низу
	$( "#add_more" ).on("click", function(){
		var destination = $("div.container div.table:last").offset().top;
		$('html').animate({ scrollTop: destination }, 1100);
	});

	//підрахунок значень кв.м.
	$("input[name$='print_width'], input[name$='print_height'], input[name$='number'],  input[name$='m_kv']").on("click change paste keyup", function() {

		var a = +$(this).closest('table').find("input[name$='print_width']").val();
		var b = +$(this).closest('table').find("input[name$='print_height']").val();
		var c = +$(this).closest('table').find("input[name$='number']").val();
 		
 		var total = parseFloat((a*b*c).toFixed(3));
 		
 		$(this).closest('table').find("input[name$='m_kv']").val(total);
	});

	// $("input[name$='print_width'], input[name$='print_height'], input[name$='number'], input[name$='m_kv'], a.remove_one, a.add_one").click(function(){

	// 	var a = +$(this).closest('table').find("input[name$='print_width']").val();
	// 	var b = +$(this).closest('table').find("input[name$='print_height']").val();
	// 	var c = +$(this).closest('table').find("input[name$='number']").val();
 		
 // 			var total = parseFloat((a*b*c).toFixed(3));
 		
 // 			$(this).closest('table').find("input[name$='m_kv']").val(total);
	// });

	$("#a0n, #a1n, #a2n, #a3n, #a4n, #a5n, #a6n, #6x3, #5_9x2_9, #4x3, #3_14x2_32, #3_14x2_3, #1_2x1_8, #1_27x1_86").click(function(){

		var a = +$(this).closest('table').find("input[name$='print_width']").val();
		var b = +$(this).closest('table').find("input[name$='print_height']").val();
		var c = +$(this).closest('table').find("input[name$='number']").val();
 		
 		var total = parseFloat((a*b*c).toFixed(3));
 		
 		$(this).closest('table').find("input[name$='m_kv']").val(total);

 		$(this).removeClass('btn-secondary').addClass('btn-danger').siblings().removeClass('btn-danger').addClass('btn-secondary');
 		$(this).closest('td').siblings().find('a.btn-danger').removeClass('btn-danger').addClass('btn-secondary');
 		$(this).closest('tr').siblings().find('a.btn-danger').removeClass('btn-danger').addClass('btn-secondary');

	});

	$("input[name$='image_url']").on("change paste keyup", function() {
	    var text = $(this).val();
		var text2 = $(this).val(text.replace(/\"/g, ""));
	});

	$("a.add_one").on("click", function(){
		var val = $(this).closest('table').find("input[name$='number']").val();
		// console.log(val);
		val_int = parseInt(val);
		total_val = val_int + 1;
		new_val = $(this).closest('table').find("input[name$='number']").val(total_val);
	});
	$("a.remove_one").on("click", function(){
		var val = $(this).closest('table').find("input[name$='number']").val();
		val_int = parseInt(val);
		total_val = val_int - 1;
		new_val = $(this).closest('table').find("input[name$='number']").val(total_val);
	});

	$("a.add_one, a.remove_one").click(function(){

		var a = +$(this).closest('table').find("input[name$='print_width']").val();
		var b = +$(this).closest('table').find("input[name$='print_height']").val();
		var c = +$(this).closest('table').find("input[name$='number']").val();
 		
 		var total = parseFloat((a*b*c).toFixed(3));
 		
 		$(this).closest('table').find("input[name$='m_kv']").val(total);
	});
 		


	$("div.table select[name$='material'] option[value='1']").css({
	'font-weight':'bold',
	// 'font-style':'italic',
	// 'color':'green',
	// console.log()
	});

	$(function () {
    $( '#main-table' ).searchable({
        // striped: true,
        // oddRow: { 'background-color': '#f5f5f5' },
        // evenRow: { 'background-color': '#fff' },
        searchType: 'fuzzy'
    });

// $( "body" ).click(function( event ) {
//   $( "body" ).html( "clicked: " + event.target.nodeName );
// });

    
    // $( '#searchable-container' ).searchable({
    //     searchField: '#container-search',
    //     selector: '.row',
    //     childSelector: '.col-xs-4',
    //     show: function( elem ) {
    //         elem.slideDown(100);
    //     },
    //     hide: function( elem ) {
    //         elem.slideUp( 100 );
    //     }
    // })
	});

	// міняємо ширину колонки "Примітка" якщо є стовпець "Ред"
	if($(".t1").length > 0)
	{
	    // alert("t1 є!");
	}
	else
	{
	     $('.t14').attr('style', 'width: 204px !important');
	}

	$("#main-table td.t5:contains('NO')").each(function() {
    	var text = $(this).text('');
    	// console.log(text);
    	// $(this).text(text.replace('dog', 'doll')); 
    });

    $("#main-table td.t5:contains('YES')").each(function() {
    	var style = $('<i class="fab fa-gripfire"></i>');
    	var text = $(this).html(style);
    	var url_color = $(this).closest('tr').find('td.t4 a').css('color', 'red');
    	// console.log(text);
    	// $(this).text(text.replace('dog', 'doll'));
    });

    // $("#main-table td.t14:contains('СТОП')").each(function() {
    // 	// var style = $('<i class="fab fa-gripfire"></i>');
    // 	var text = $(this).closest('tr').find("td.t5").html("STOP");
    // 	var stopDtyle = text.addClass("stopStatus")
    // 	// console.log(text);
    // 	// $(this).text(text.replace('dog', 'doll'));
    // });

    var statusStop = $("#main-table td.t14:contains('СТОП')").closest('tr').find("td.t5").attr('id', 'stopStatus').html("STOP");

    $("#main-table td:contains('RIP')").each(function() {
    	var pencil = $(this).find('a').css("color","#FFA500");
    });

    $("#main-table td:contains('Виконано')").each(function() {
    	// var pencil = $(this).find('a').css("color","green");
    	var del_pencil = $(this).find('a').remove();
    	$(this).css("padding-left", "18px");
    });

    $("#main-table td:contains('Виконано')").closest('tr').find('td:first a').remove();

    //рахувальниця на сторінці home
	var total = 0;
	$("#main-table").on("click", "td.t7", function(){
		$(this).toggleClass('clicked');
		$(this).toggleClass("table-info");
	
		if ($(this).hasClass('table-info')){
			val = parseInt($(this).text());
				total = parseInt(total+val);
				// console.log(total);
		}else{
			val2 = parseInt($(this).text());
				total = parseInt(total-val2);
				// console.log(total);
		}
		new_summ = $("#main-table th.t7").html(total);
	});

	$("#main-table").on("click", " td.t3", function(){
		$(this).closest("tr").toggleClass("colorBlue");
	})

	//Розмальовка статусу "Виконано"
    var statusOleg = $("#main-table td.t12:contains('Олег')").closest('tr').find("td:contains('Виконано')").addClass('table-success');
    var statusPetro = $("#main-table td.t12:contains('Петро')").closest('tr').find("td:contains('Виконано')").addClass('table-warning');
    var statusSerg = $("#main-table td.t12:contains('Сергій')").closest('tr').find("td:contains('Виконано')").addClass('table-danger');
    var statusSerg = $("#main-table td.t12:contains('Роман')").closest('tr').find("td:contains('Виконано')").css('background-color', '#FFB775');

    $('#main-table .t12:contains("None")').html('');

    //Форматка
    $('#main-table td.t6:contains("0.841 x 1.189")').html('A0');
    $('#main-table td.t6:contains("0.594 x 0.841")').html('A1');
    $('#main-table td.t6:contains("0.42 x 0.594")').html('A2');
    $('#main-table td.t6:contains("0.297 x 0.42")').html('A3');
    $('#main-table td.t6:contains("0.21 x 0.297")').html('A4');
    $('#main-table td.t6:contains("0.148 x 0.21")').html('A5');
    $('#main-table td.t6:contains("0.105 x 0.148")').html('A6');

    //маркування нового дня
 

    $("#btnExport").click(function () {
        $("#main-table").btechco_excelexport({
            containerid: "tblExport"
        });
    });
  
 });

var ts = $("select[name$='name_of_camp']").val();
if (ts == 'Сюжет'){
	$("select[name$='name_of_camp']").css('color', 'red');
}

$("select[name$='name_of_camp'] option:first, select[name$='material'] option:first, select[name$='manager'] option:first, select[name$='status'] option:first").css({
	'font-weight':'bold',
	'font-style':'italic',
	// 'color':'green',
});

