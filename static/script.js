/*
Internal script for Pizza time
*/
$(document).ready(function() {
     $.get('/nav', function(nav){
          $('#nav').html(nav)
     })
     //toggle the edit the order summary row
     $('#edit').click(function(){
          $('.editForm').toggle();
     })
})
