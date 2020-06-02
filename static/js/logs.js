var pageLoaded = window.addEventListener('load', function () {
  $('div.spinner-wrapper').css('display', 'none');
  $('div.loadingio-spinner-blocks-bviunr6j92k').css('display', 'none');
  $('div.spinner-box').css('display', 'none');
  $('div.table-row').css('display', 'table');
});

var today = new Date(new Date().getFullYear(), new Date().getMonth(), new Date().getDate());
  $('#id_date_from').datepicker({
      uiLibrary: 'bootstrap4',
      iconsLibrary: 'fontawesome',
      locale: 'ua-ua',
      format: 'yyyy-mm-dd'
  });

  $('#id_date_to').datepicker({
      uiLibrary: 'bootstrap4',
      iconsLibrary: 'fontawesome',
      locale: 'ua-ua',
      format: 'yyyy-mm-dd'
  });

  $('button#get_db_logs').on('click', function () {
      if(($('input#id_date_from').val() != '') && ($('input#id_date_to').val() != '')){
          $('div.table-row').css('display', 'none');
          $('div.spinner-box').css('display', 'block');
      };
  });

  $('a.update_logs').on('click', function () {
      $('div.spinner-wrapper').css('display', 'block');
      $('div.loadingio-spinner-blocks-bviunr6j92k').css('display', 'block');
  });
