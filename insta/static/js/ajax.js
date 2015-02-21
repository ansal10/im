/**
 * Created by amd on 2/11/15.
 */

function Ajax(url , type , id){
    $.ajax({
        url:url,
        type:type,
        success: function(result){
            $('#id').html(result);
        }
    });
}