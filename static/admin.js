/*
Admin script for Pizza time
*/
$(document).ready(function() {
     $.get('/admin/nav', function(nav){
          $('#aNav').html(nav)
     });
     $(function () {
          $('#tabs').tabs();
     });

     /*
     $('#tableData tbody tr').click(function() {
          var rowData = $(this).children('td').map(function(){
               return $(this).text();
          }).get();
          console.log(rowData);
     })*/
     $('#tableData').find('#btn_save').hide();
     $('#tableData').find('#btn_cancel').hide();

     $('#tableData').on('click','#update_btn', function(event) {
        event.preventDefault();

        var tb_row = $(this).closest('tr');
        var row_id = tb_row.attr('row_id');
        //console.log(row_id)

        tb_row.find('#btn_save').show();
        tb_row.find('#btn_cancel').show();

        tb_row.find('#update_btn').hide();

        tb_row.find('.rowData')
		.attr('contenteditable', 'true')
		.attr('edit_type', 'button')

        var arr = {}
        tb_row.find('.rowData').each(function(index, val){
             var col_name = $(this).attr('col');
             var col_val = $(this).html():
             arr[col_name]=col_val; 
        })



     });
});
