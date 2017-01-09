$(document).ready(function(){
    var deleters = $(".delete");
    deleters.on("click", function(e){
        // send ajax request to delete this expense
        $.ajax({
            url: $(this).attr("data") + '/delete',
            success: function(){
                console.log("deleted");
                location.href = '/'
            }
        });        
    });
});

