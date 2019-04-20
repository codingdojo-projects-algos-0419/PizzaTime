/*
Admin script for Pizza time
*/
$(document).ready(function() {
     $.get('/admin/nav', function(nav){
          $('#aNav').html(nav)
     })

})
