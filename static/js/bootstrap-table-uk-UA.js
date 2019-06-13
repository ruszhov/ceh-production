(function (global, factory) {
  if (typeof define === "function" && define.amd) {
    define([], factory);
  } else if (typeof exports !== "undefined") {
    factory();
  } else {
    var mod = {
      exports: {}
    };
    factory();
    global.bootstrapTableUkUA = mod.exports;
  }
})(this, function () {
  'use strict';

  /**
   * Bootstrap Table Ukrainian translation
   * Author: Vitaliy Timchenko <vitaliy.timchenko@gmail.com>
   */
  (function ($) {
    $.fn.bootstrapTable.locales['uk-UA'] = {
      formatLoadingMessage: function formatLoadingMessage() {
        return 'Завантаження‚ зачекайте, будь ласка...';
      },
      formatRecordsPerPage: function formatRecordsPerPage(pageNumber) {
        return pageNumber + ' \u0437\u0430\u043F\u0438\u0441\u0456\u0432 \u043D\u0430 \u0441\u0442\u043E\u0440\u0456\u043D\u043A\u0443';
      },
      formatShowingRows: function formatShowingRows(pageFrom, pageTo, totalRows) {
        return '\u041F\u043E\u043A\u0430\u0437\u0430\u043D\u043E \u0437 ' + pageFrom + ' \u043F\u043E ' + pageTo + '. \u0412\u0441\u044C\u043E\u0433\u043E: ' + totalRows;
      },
      formatSearch: function formatSearch() {
        return 'Пошук';
      },
      formatNoMatches: function formatNoMatches() {
        return 'Жодних даних не знайдено';
      },
      formatRefresh: function formatRefresh() {
        return 'Оновити';
      },
      formatToggle: function formatToggle() {
        return 'Переключити вигляд';
      },
      formatColumns: function formatColumns() {
        return 'Стовпці';
      },
      formatClearFilters: function formatClearFilters() {
        return 'Очистити фільтри';
      },
      formatMultipleSort: function formatMultipleSort() {
        return 'РЎРѕСЂС‚СѓРІР°РЅРЅСЏ Р·Р° РєС–Р»СЊРєРѕРјР° СЃС‚РѕРІРїС†СЏРјРё';
      },
      formatAddLevel: function formatAddLevel() {
        return 'Р”РѕРґР°С‚Рё СЂС–РІРµРЅСЊ';
      },
      formatDeleteLevel: function formatDeleteLevel() {
        return 'Р’РёРґР°Р»РёС‚Рё СЂС–РІРµРЅСЊ';
      },
      formatColumn: function formatColumn() {
        return 'РЎС‚РѕРІРїРµС†СЊ';
      },
      formatOrder: function formatOrder() {
        return 'Порядок';
      },
      formatSortBy: function formatSortBy() {
        return 'Сортувати';
      },
      formatThenBy: function formatThenBy() {
        return 'РїРѕС‚С–Рј Р·Р°';
      },
      formatSort: function formatSort() {
        return 'Сортувати';
      },
      formatCancel: function formatCancel() {
        return 'Відмінити';
      },
      formatDuplicateAlertTitle: function formatDuplicateAlertTitle() {
        return 'Р”СѓР±Р»СЋРІР°РЅРЅСЏ СЃС‚РѕРІРїС†С–РІ!';
      },
      formatDuplicateAlertDescription: function formatDuplicateAlertDescription() {
        return 'Р’РёРґР°Р»С–С‚СЊ, Р±СѓРґСЊ Р»Р°СЃРєР°, РґСѓР±Р»СЋСЋС‡РёР№ СЃС‚РѕРІРїРµС†СЊ, Р°Р±Рѕ Р·Р°РјС–РЅС–С‚СЊ Р№РѕРіРѕ РЅР° С–РЅС€РёР№.';
      }
    };

    $.extend($.fn.bootstrapTable.defaults, $.fn.bootstrapTable.locales['uk-UA']);
  })(jQuery);
});