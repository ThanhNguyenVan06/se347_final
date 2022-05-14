

$(document).ready(function() {
    
    $(".btn").click(function(){
        $.ajax({
            url: "cart/",
            type: "Get",
            data:{
                "button_value" : $(this).val(),
            },
            success: function(data){
                if (data.count != -1){

                    $(".cart_count").html(data.count);
                }
                else {
                    location.href = "http://127.0.0.1:8000/account/login/"
                }
                
            }
        })
    })
})