$( document ).ready(function() {
  $('.materialorder input, .materialorder select').each(function(){
		$(this).blur(function(){
		    tmpval = $(this).val();
		    if(tmpval == '') {
		        $(this).addClass('empty');
		        $(this).removeClass('not-empty');
		    } else {
		        $(this).addClass('not-empty');
		        $(this).removeClass('empty');
		    }
		});
		$(this).is(function(){
	    tmpval = $(this).val();
		    if(tmpval == '') {
		        $(this).addClass('empty');
		        $(this).removeClass('not-empty');
		    } else {
		        $(this).addClass('not-empty');
		        $(this).removeClass('empty');
		    }
		});
	});
});

$("body").on('click change paste keyup', function(){
	$('.materialorder input, .materialorder select').each(function(){
		$(this).blur(function(){
		    tmpval = $(this).val();
		    if(tmpval == '') {
		        $(this).addClass('empty');
		        $(this).removeClass('not-empty');
		    } else {
		        $(this).addClass('not-empty');
		        $(this).removeClass('empty');
		    }
		});
		$(this).is(function(){
	    tmpval = $(this).val();
		    if(tmpval == '') {
		        $(this).addClass('empty');
		        $(this).removeClass('not-empty');
		    } else {
		        $(this).addClass('not-empty');
		        $(this).removeClass('empty');
		    }
		});
	});

	//підрахунок значень кв.м. матеріалу
	$("input[name$='material_width'], input[name$='material_height'], input[name$='number_of_material']").on("click change paste keyup", function() {
		var a = +$(this).closest('div.tab-content').find("input[name$='material_width']").val();
		var b = +$(this).closest('div.tab-content').find("input[name$='material_height']").val();
		var c = +$(this).closest('div.tab-content').find("input[name$='number_of_material']").val(); 		
		var total = parseFloat((a*b*c).toFixed(3)); 		
		$(this).closest('div.tab-content').find("input[name$='m_kv_of_material']").val(total);
		$(this).closest('div.tab-content').find("input[name$='m_kv_of_material']").addClass('not-empty');
	});
	
	//підрахунок значень л. фарб
	$("input[name$='litr_of_paint'], input[name$='number_of_litres']").on("click change paste keyup", function() {
		var a = +$(this).closest('div.tab-content').find("input[name$='litr_of_paint']").val();
		var b = +$(this).closest('div.tab-content').find("input[name$='number_of_litres']").val(); 		
		var total = parseFloat((a*b).toFixed(3)); 		
		$(this).closest('div.tab-content').find("input[name$='all_litres']").val(total);
		$(this).closest('div.tab-content').find("input[name$='all_litres']").addClass('not-empty');
	});

	//підрахунок значень "іншого"
	$("input[name$='packing_of_other'], input[name$='number_of_other']").on("click change paste keyup", function() {
		var a = +$(this).closest('div.tab-content').find("input[name$='packing_of_other']").val();
		var b = +$(this).closest('div.tab-content').find("input[name$='number_of_other']").val(); 		
		var total = parseFloat((a*b).toFixed(3)); 		
		$(this).closest('div.tab-content').find("input[name$='all_of_other']").val(total);
		$(this).closest('div.tab-content').find("input[name$='all_of_other']").addClass('not-empty');
	});
});

// стилізаця помилок
$('.errorlist').closest('.group').find('input').css({'border-bottom':'2px solid red', 'color':'red'});
$('.errorlist').closest('.group').find('span').remove();

$('.add_more_materialorder').click(function(event){

		//Берем значення select з попередньої таблиці
		var previous = $("div.container div.selector-to-clone:last").prev("div.selector-to-clone");
		var prevInvoice = previous.find("input[name$='invoice']").val();
		var prevProvider = previous.find("select[name$='provider'] :selected").val();
		// console.log(prevInvoice);
		// console.log(prevProvider);

		var current = $("div.container div.selector-to-clone:last");
		var curInvoice = current.find("input[name$='invoice']").val(prevInvoice);
		var curProvider = current.find("select[name$='provider']").val(prevProvider);
		// var curDescription = current.find("textarea[name$='description']");
		// var allprevDescription = curDescription.prevAll("textarea[name$='description']");
		// console.log(allprevDescription);
		// приховуємо полярахунок і постачальник у всіх клонованих табах
		var hideInvoice = current.find("div.group.invoice, div.group.provider, div.button-group.add-provider-button").addClass('hidden');

		// завжди активна перша вкладка табів
		var remActiveTabs = current.find("div.nav a").removeClass("active show");
		var addActiveTabs = current.find("div.nav a:first").addClass("active");

		//завжди активна перша панель табів
		var remActiveTabPane = current.find("div.tab-content div.tab-pane").removeClass("active");
		var addActiveTabPane = current.find("div.tab-pane:first").addClass("active show");

		//перемотуємо сторінку донизу при додаванні ще одного замовлення
		var destination = $("div.container div.selector-to-clone:last").offset().top;
		$('html').animate({ scrollTop: destination }, 1100);

	});

// Синхронізація значень для рахунку еталонного і всіх що йдуть нижче
$("input[name$='invoice']").on("change paste keyup", function(){
	var invoice = $("div.container div.selector-to-clone");
	var etalonInvoice = invoice.find("input[name$='invoice']").val();
	var allInvoice = invoice.find("input[name$='invoice']").val(etalonInvoice);
});

// Синхронізація значень для постачальника еталонного і всх що йдуть нижче
$("select[name$='provider']").on("mouseup", function(){
	var provider = $("div.container div.selector-to-clone");
	var etalonProvider = provider.find("select[name$='provider']").val();
	console.log(etalonProvider);
	var allProvider = provider.find("select[name$='provider']").val(etalonProvider);
});


// ЗАГАЛЬНА ТАБЛИЦЯ

// статус оплачено-неоплачено
// $('.materialorder .m9:contains("None")').html('Неоплачено');
// $('.materialorder .m9:contains("True")').html('Оплачено');

// ціни в таблиці
$('.materialorder .m_kv_of_material:contains("None")').closest('span').remove();
$('.materialorder .all_litres:contains("None")').closest('span').remove();
$('.materialorder .all_of_other:contains("None")').closest('span').remove();
$('.materialorder .total_of_material:contains("None")').closest('span').remove();
$('.materialorder .total_of_paint:contains("None")').closest('span').remove();
$('.materialorder .total_of_other:contains("None")').closest('span').remove();
// $('.materialorder .m7:contains("None")').html('0');

$("#search-toggle").click(function() {
  $('.transform').toggleClass('transform-active');
});

$(".clean-material").click(function(event){
	$(this).closest(".search-box").find("input").val('');
	$(this).closest(".search-box").find("select").val('');
});
$(".close-material, .search-material").click(function(event){
	$('.transform').toggleClass('transform-active');
});
$(".search-box").find("i.gj-icon").remove();
$(".search-box").find(".border-left-0").html("<i class='fas fa-calendar-alt'></i>");
$(".search-box").find("#id_created_0, #id_created_1").css("width", "197");

$("select[name$='provider'] option:first, select[name$='paint'] option:first, select[name$='other'] option:first, select[name$='paid'] option:first").css({
	'font-weight':'bold',
	'font-style':'italic',
	// 'color':'green',
});

// міняємо ширину колонки "Примітка" якщо є стовпець "Ред"
	if($("#materialorder .m1").length > 0)
	{
	    // alert("m1 є!");
	}
	else
	{
	     $('.m8').attr('style', 'width: 240px !important');
	    // alert("no");
	}
$("#materialorder td.m9 span:contains('True')").each(function() {
    	var paid = $(this).html('<span id="paid"><i class="far fa-money-bill-alt"></i></span> Оплачено');
    	var del_pencil = $(this).closest('td').find('a').remove();
    	var paid_color = $(this).closest('td').find('i').css('color', 'green');	
});
$("#materialorder td.m9 span:contains('None')").each(function() {
    	var paid = $(this).html('Неоплачено');
    	var url_color = $(this).closest('tr').find('td.m9 a').css('color', 'red');    	
});
$("#materialorder td:contains('Оплачено')").closest('tr').find('td:first a').remove();
$('#materialorder .m6:contains("None"), #materialorder .m7:contains("None"), #materialorder .m11:contains("None")').html('');

// рахуємо None
// $( document ).ready(function() {
// 	$("materialorder tr").each(function(){
// 		nonecount = $(this).find("m6:contains('None')").size();
// 		if( nonecount == 2){
// 			$("td[rowspan].m1").attr("rowspan", function(i, rs) { return rs - 1 })
// 		}
// 		else
// 		{

// 		}
// 	});
// })


// $("#materialorder .m6:contains('None')").count();

// $('.materialorder input, .materialorder select').each(function(){
// 		$(this).blur(function(){
// 		    tmpval = $(this).val();
// 		    if(tmpval == '') {
// 		        $(this).addClass('empty');
// 		        $(this).removeClass('not-empty');
// 		    } else {
// 		        $(this).addClass('not-empty');
// 		        $(this).removeClass('empty');
// 		    }
// 		});
// 		$(this).is(function(){
// 	    tmpval = $(this).val();
// 		    if(tmpval == '') {
// 		        $(this).addClass('empty');
// 		        $(this).removeClass('not-empty');
// 		    } else {
// 		        $(this).addClass('not-empty');
// 		        $(this).removeClass('empty');
// 		    }
// 		});
// 	});