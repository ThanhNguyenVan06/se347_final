

$(document).ready(function() {
    
    $(".btn").click(function(){
        $.ajax({
            url: "cart/",
            type: "Get",
            data:{
                "button_value" : $(this).val(),
            },
            success: function(data){
               $(".cart_count").html(data.count);
            }
        })
    })
})