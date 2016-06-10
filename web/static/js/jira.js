$(document).ready(function(){
    updateTikets();
});
var client_id=1; 
function updateTikets(){
    $.getJSON('get_tickets', {
        'client': client_id
    }, function(data) {
        console.log(data);
    });
}