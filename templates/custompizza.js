// Note: This file must be used as a Jinja template include
<script>
$(function(){
      var order_id={{order.id}};

      var price_size={
           {% for size in sizes %}
           {{size.id}}:{{size.price}},
           {% endfor %}
           placeholder:0
      };
      var scaling_size={
           {% for size in sizes %}
                {% if size.scaling %}
           {{size.id}}:{{size.scaling}},
                {% else %}
           {{size.id}}:1,
                {% endif %}
           {% endfor %}
           placeholder:0
      }

      var price_style={
           {% for style in styles %}
           {{style.id}}:{{style.price}},
           {% endfor %}
           placeholder:0
      };
      var price_topping={
           {% for topping in toppings_menu %}
           {{topping.id}}:{{topping.price}},
           {% endfor %}
           placeholder:0
      };

      // Calculates a live price of a pizza with the current configuration
      //$("#pizza_config").on("change","[name='size']",function(){
      $("#size_select").change(function(){
           var scaling=scaling_size[$("[name='size']").val()]
           //console.log(scaling);
           $(".topping_price").each(function(i){
                //console.log($(this).attr("topping_id"));
                //console.log(price_topping[$(this).attr("topping_id")]);
                //console.log(scaling);
                let price=price_topping[$(this).attr("topping_id")]*scaling;
                $(this).text("$"+price.toFixed(2));
           })
      });

      function calc_preview_price(){
           let preview_price=(price_size[$("[name='size']").val()]+ price_style[$("[name='style']").val()]);
           $("[name='topping']").each(function(i){
                if ($(this).prop("checked")){
                     //console.log($(this).val());
                     preview_price+=price_topping[$(this).val()]
                }
           })
           //console.log(preview_price);
           $("#preview_price").text("$"+preview_price.toFixed(2)+" ea");
      }

      $("#pizza_config").children().change(calc_preview_price);
      calc_preview_price();

      // Remove a pizza from the order table
      $("tbody").on("click",".remove_pizza",function(e){
           console.log("delete pizza " +$(this).attr("pizza_id"));
           let pizza_id=$(this).attr("pizza_id");
           $.ajax({
                method:'POST',
                url:"/remove/pizza",
                data:{json: JSON.stringify({'pizza_id':$(this).attr("pizza_id")})}
           })
           .done(function(resp_data){
                $.ajax({
                     method: "GET",
                     url:"/total"
                }).done(function(resp){
                     $("#order_total").text("Total: $"+resp);
                });
           });
           $("[tr_pizza_id="+pizza_id+"]").remove();
      });

      // Add a pizza to the order
      $("#pizza_config").submit(function(){
           $.ajax({
                method: $(this).attr("method"),
                url: $(this).attr("action"),
                data:$(this).serialize()
           })
           .done(function(resp_data){
                $("tbody").append(resp_data);
                $.ajax({
                     method: "GET",
                     url:"/total"
                }).done(function(resp){
                     $("#order_total").text("Total: $"+resp);
                });
           });
           return false;
      });

      // Clear all the pizzas from the current order
      $("#clear_order").click(function(){
           //console.log("clear order");
           $.ajax({
                method: "POST",
                url: "/remove/pizzas",
                data: {json: JSON.stringify({"order_id":order_id})}
           })
           $("tbody").html(null);
           $("#order_total").text("Total: $0.00");
      });
 });

</script>