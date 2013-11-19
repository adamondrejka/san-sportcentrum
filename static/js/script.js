/**
 * Created by adam on 18.11.13.
 */
$("#datepicker").datepicker();

function changeSportoviste(){
    $.ajax({
        url: "/ajax/get_sportoviste/",
        data: {
            id_sportovni_centrum: $("sportovni_centrum").value()
        }
    }).done(function(data){
            for (var i=0; i< data.result.length; i++) {

            }
        })
}