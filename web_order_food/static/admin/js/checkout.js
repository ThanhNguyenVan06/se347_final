$(document).ready(function() {
    $.ajax({
        url:'checkout_process/',
        type:'GET',
        success: function(data){
            if (data == 0){
                window.location = "http://127.0.0.1:8000/checkout/emptycart"; 
            }
            function cart_not_empty(){
            var total = 0;
            // function set_table(total){
                for (var i=0; i<data.arr_items.length; i++){
                    $(".table_bill").append("<tr class = \""+i+"\">"+
                    "<td class = \"name_food\">"+data.arr_items[i].name_food+"</td>"+
                    "<td class = \"quantity\">"+"<input type=\"number\" class=\"quantity_\" name=\""+data.arr_items[i].id_food+"\" min=\"1\"  value = \""+data.arr_items[i].quantity +"\">"+"</td>"+
                    "<td class = \"price\">"+data.arr_items[i].quantity * data.arr_items[i].price+"</td>"+
                    "<td><button class=\"btnDelete\">Delete</button></td>"
                    +"</tr>"               
                    );
                    total += data.arr_items[i].quantity * data.arr_items[i].price
                }
            // }
            //setTimeout(set_table,500,total);

            var total_text = document.getElementById("total");
            total_text.innerHTML = total;
            var input_quantity = document.getElementsByClassName("quantity_");
            var price = document.getElementsByClassName("price");
            
            // for (let i = 0; i < input_quantity.length; i++) {
               
            //     item = document.getElementsByClassName("quantity_")[i]
            //     item.addEventListener('change',(event) =>{
            //         console.log(i)
            //         price[i].innerHTML = data.arr_items[i].price*event.target.value;                  
            //     })
            // }
            
            $(".table_bill").on("click",'.btnDelete',function(){
                $(this).closest("tr").remove();
                var price = document.getElementsByClassName("price");
                
                total = 0                         
                for (let j = 0; j < price.length; j++) {
                    item_temp = document.getElementsByClassName("price")[j]
                    total += parseInt(item_temp.innerHTML);

                    console.log(total);
                } 
                total_text.innerHTML = total;
                
            });
            $(".quantity_").on("change", function(){
                index = parseInt(this.name)
                //price[index-1].innerHTML = data.arr_items[index-1].price*this.value;
                console.log(data.arr_items[index-1].price*this.value)
                $(this).closest('tr').find(".price").text(data.arr_items[index-1].price*this.value)
                console.log($(this).closest('tr').find(".price").text(data.arr_items[index-1].price*this.value));
                total = 0
                for (let j = 0; j < price.length; j++) {
                    item_temp = document.getElementsByClassName("price")[j]
                    total += parseInt(item_temp.innerHTML);

                    console.log(total);
                } 
                total_text.innerHTML = total;
            })
        }
        setTimeout(cart_not_empty,100)
    }
    
    }); 
       
})

