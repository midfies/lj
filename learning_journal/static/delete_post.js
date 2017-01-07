$(document).ready(function(){
    var deleters = $(".delete");
    deleters.on("click", function(e){
        // send ajax request to delete this expense
        $.ajax({
            url: 'journal/' + $(this).attr("data") + '/delete',
            success: function(){
                console.log("deleted");
            }
        });        
        // fade out expense
        this_row = $(this.parentNode.parentNode);
        // delete the containing row
        this_row.animate({
            opacity: 0
        }, 500, function(){
            $(this).remove();
        })
    e.preventDefault();   
    });
});