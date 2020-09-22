document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.modal');
    var instances = M.Modal.init(elems, options);
});

$('.materialert .close-alert').click(function (){
    $(this).parent().hide('slow');
});

var el = document.querySelector('.tabs');
var instance = M.Tabs.init(el, {});
document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('.modal');
  var instances = M.Modal.init(elems);
});
