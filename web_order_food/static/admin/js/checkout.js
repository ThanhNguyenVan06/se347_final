$(document).ready(function() {
    $.ajax({
        url:'checkout_process/',
        type:'GET',
        success: function(data){
            for (var i=0; i<data.arr_items.length; i++){
                $(".table_bill").append("<tr class = \"order_"+data.arr_items[i].id_food+"\">"+
                "<td class = \"name_food\">"+data.arr_items[i].name_food+"</td>"+
                "<td class = \"quantity\">"+"<input type=\"number\" class=\"quantity_\" name=\""+data.arr_items[i].id_food+"\" min=\"1\"  value = \""+data.arr_items[i].quantity +"\">"+"</td>"+
                "<td class = \"price\">"+data.arr_items[i].quantity * data.arr_items[i].price+"</td>"+
                "<td><button class=\"btnDelete\">Delete</button></td>"
                +"</tr>"               
                );
            }
            var input_quantity = document.getElementsByClassName("quantity_");
            var price = document.getElementsByClassName("price");
    
            for (let i = 0; i < input_quantity.length; i++) {
               
                item = document.getElementsByClassName("quantity_")[i]
                item.addEventListener('change',(event) =>{
                    price[i].innerHTML = data.arr_items[i].price*event.target.value;                  
                    
                })
            }
            $(".table_bill").on("click",'.btnDelete',function(){
                $(this).closest("tr").remove();
            });

        }
        
    }); 
 
       
})

