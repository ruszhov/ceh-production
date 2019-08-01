/*! jQuery Searchable v1.0.0 by Stidges (http://twitter.com/stidges) | MIT */
!function(a){function b(b,c){this.$element=a(b),this.settings=a.extend({},d,c),this.init()}var c="searchable",d={selector:"tbody tr",childSelector:"td",searchField:"#search",striped:!1,oddRow:{},evenRow:{},hide:function(a){a.hide()},show:function(a){a.show()},searchType:"default"};b.prototype={init:function(){this.$searchElems=a(this.settings.selector,this.$element),this.$search=a(this.settings.searchField),this.matcherFunc=this.getMatcherFunction(this.settings.searchType),this.bindEvents(),this.updateStriping()},bindEvents:function(){var b=this;this.$search.on("change keyup",function(){b.search(a(this).val()),b.updateStriping()}),""!==this.$search.val()&&this.$search.trigger("change")},updateStriping:function(){var b=this,c=["oddRow","evenRow"],d=this.settings.selector+":visible";this.settings.striped&&a(d,this.$element).each(function(d,e){a(e).css(b.settings[c[d%2]])})},search:function(b){var c,d,e,f,g,h,i,j;if(0===a.trim(b).length)return this.$searchElems.css("display",""),void this.updateStriping();for(d=this.$searchElems.length,c=this.matcherFunc(b),i=0;d>i;i++){for(h=a(this.$searchElems[i]),e=h.find(this.settings.childSelector),f=e.length,g=!0,j=0;f>j;j++)if(c(a(e[j]).text())){g=!1;break}g===!0?this.settings.hide(h):this.settings.show(h)}},getMatcherFunction:function(a){return"fuzzy"===a?this.getFuzzyMatcher:"strict"===a?this.getStrictMatcher:this.getDefaultMatcher},getFuzzyMatcher:function(a){var b,c=a.split("").reduce(function(a,b){return a+"[^"+b+"]*"+b});return b=new RegExp(c,"gi"),function(a){return b.test(a)}},getStrictMatcher:function(b){return b=a.trim(b),function(a){return-1!==a.indexOf(b)}},getDefaultMatcher:function(b){return b=a.trim(b).toLowerCase(),function(a){return-1!==a.toLowerCase().indexOf(b)}}},a.fn[c]=function(d){return this.each(function(){a.data(this,"plugin_"+c)||a.data(this,"plugin_"+c,new b(this,d))})}}(jQuery,window,document);


// function myFunction() {
//   var input, filter, table, tr, td, i;
//   input = document.getElementById("search");
//   filter = input.value.toUpperCase();
//   table = document.getElementById("main-table");
//   tr = table.getElementsByTagName("tr");
//   for (i = 0; i < tr.length; i++) {
//     td = tr[i].getElementsByTagName("td")[0];
//     if (td) {
//       if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
//         tr[i].style.display = "";
//       } else {
//         tr[i].style.display = "none";
//       }
//     }       
//   }
// }