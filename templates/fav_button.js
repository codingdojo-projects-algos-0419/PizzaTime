<script>
$(function(){
     $("#fav_button").click(function(){
        console.log("favorite");
        var fav_data={
            order_id: {{order.id}},
            customer_id: {{order.customer.id}}
        };
        $.ajax(
            {method:"Post",
            url:"/favorite/update",
            data: { json: JSON.stringify(fav_data)}
            //data: { 'customer':{{order.customer.id}},'order_id':{{order.id}} }
            }
        ).done(function(response){
            $("#fav_button").text("Made your Fav!");
            $("#fav_button").removeClass("btn-warning");
            $("#fav_button").addClass("btn-success");
            $("#fav_button").attr("disabled", true); 
        });
    });
});
</script>