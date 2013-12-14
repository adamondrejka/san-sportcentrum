/**
 * Created by adam on 18.11.13.
 */
$("#datepicker").datepicker();

var is_admin;

$(document).ready(function(){
    changeSportovniCentrum();



    $("#reservation_form").on('submit', function(e) {
        e.preventDefault();
        var postData = $(this).serializeArray();
        var formUrl = $(this).attr("action");

        $.ajax({
            url: formUrl,
            type: "POST",
            data: postData
        }).done(function(data) {
            if(data.result == 'ok') {
                changeSportoviste(null);
                alert('Úspěšně rezervováno');
            }
            else if(data.result== 'nomoney'){
                alert('Nemáte na účtě dostatek peněz');
            }

            $("#reservation-modal").modal('hide');


        });

    });

    $("#datepicker").change(function(){
        changeSportoviste(null);
    });

    $("#sportovni_centrum").change(function(){
        changeSportovniCentrum();
    });


    is_admin = ($("#is_admin").val() == "1")? true : false;

});

function pay(){
    $.ajax({
        url: "/ajax/pay/?rezervace_id="+$("#rezervace_id").val()

    }).done(function(data){
            if (data.result == 'ok') {
                changeSportoviste(null);
                alert("Úspěšně zaplaceno");
            }
            else if (data.result == 'alreadypaid') {
                changeSportoviste(null);
                alert("Rezervace jiz byla zaplacena");
            }
            else {
                alert("Nedostatek peněz na kontě");
            }

            $("#reservation-modal").modal('hide');
        })
}
function cancelReservation(){
    $.ajax({
        url: "/ajax/delete_reservation/?rezervace_id="+$("#rezervace_id").val()

    }).done(function(data){
            if (data.result == 'ok') {
                changeSportoviste(null);
                alert("Úspěšně zrušeno");
            }

            $("#reservation-modal").modal('hide');
        })
}


function changeSportovniCentrum(){
    $.ajax({
        url: "/ajax/get_sportoviste/?id_sportovni_centrum="+$("#sportovni_centrum").val()

    }).done(function(data){
            console.log(data);

            var txt = '<div class="btn-group" data-toggle="buttons">';

            for (var i=0; i< data.result.length; i++) {
                if (i==0)
                    txt += ' <label class="btn btn-primary"><input type="radio" name="options" id="option1" checked onchange="changeSportoviste('+data.result[i].id+')" value="'+data.result[i].id+'">' + data.result[i].nazev  +'</label>';
                else
                    txt += ' <label class="btn btn-primary"><input type="radio" name="options" id="option2" onchange="changeSportoviste('+data.result[i].id+')" value="'+data.result[i].id+'">' + data.result[i].nazev  +'</label>'
            }

            txt += '</div>';

            $("#sportoviste").html(txt);
            $('.btn-group').button();

            $("#rezervace").html('');

        })
}

function changeSportoviste(id_sportoviste) {
    var date = $("#datepicker").val();

    if (id_sportoviste == null)
        id_sportoviste = $("input:radio[name=options]:checked").val();

    $.ajax({
        url: "/ajax/get_calendar/?id_sportoviste="+id_sportoviste+"&datum="+date

    }).done(function(data){
            var txt1 = '<div class="reservation-labels"><div>---</div>';

            // vykresli mista sportoviste do leveho panelu
            for (var i=0; i< data.result_mista.length; i++) {
               txt1 += '<div>' + data.result_mista[i].nazev + '</div>';
            }

            txt1 += '</div>';

            txt2 = '<div class="reservation-units"><div class="reservation-unit-holder"><div class="reservation-row">';

            var sportoviste = data.result_sportoviste;
            var num_units = (sportoviste.konec_provozu - sportoviste.zacatek_provozu) / sportoviste.interval_vypujcek;

            // vykresli hodiny
            for (var i=0; i< num_units; i++) {

               var time_minutes = sportoviste.zacatek_provozu + (i * sportoviste.interval_vypujcek);
               txt2 += '<div class="reservation-unit reservation-times">' + getTimeString(time_minutes) + '</div>';

            }

            txt2 += '</div>';

            for (var i=0; i< data.result_mista.length; i++) {
                txt2 += '<div class="reservation-row">';
               for (var j=0; j< num_units; j++) {
                   var time_minutes = sportoviste.zacatek_provozu + (j * sportoviste.interval_vypujcek);
                   txt2 += '<div class="reservation-unit reservation-clickable" id="unit_'+ data.result_mista[i].id + '_' + time_minutes+'" data-minutes="'+ time_minutes+'" data-misto=' + data.result_mista[i].id +'></div>';

                }

               txt2 += '</div>';
            }

            txt2 += '</div></div>';


            $("#rezervace").html(txt1 + txt2);
            $("#interval").val(sportoviste.interval_vypujcek);

            $(".reservation-clickable").click(function(e){
                var sel_unit = e.target;

                var is_edited = false;
                if (sel_unit.dataset.reservationid != undefined)
                    is_edited = true;

                var misto = sel_unit.dataset.misto;

                if (!is_edited){
                    // nova rezervace
                     $("#admin_buttons").hide();
                    $("#rezervace_datum_txt").val($('#datepicker').val());
                    $("#rezervace_datum").val($('#datepicker').val());
                    var minutes = e.target.dataset.minutes;
                    $("#rezervace_od_txt").val(getTimeString(minutes));
                    $("#rezervace_od").val(minutes);
                    $("#sportoviste_misto").val(misto);
                    $("#rezervace_id").val('');
                    $("#cena_interval").val(sportoviste.cena_interval);
                    $("#reservation-modal").modal();

                    $("#rezervace_do")
                            .find("option")
                            .remove();

                    for (var i=1; i<4; i++) {

                        var new_min = parseInt(minutes) + i* sportoviste.interval_vypujcek;

                        $("#rezervace_do")
                            .append($("<option></option>")
                            .attr("value", new_min)
                            .text(getTimeString(new_min)));

                    }
                }
                else if(is_edited && is_admin) {
                    // uprava rezervace
                    $("#admin_buttons").show();
                    $("#rezervace_datum_txt").val(sel_unit.dataset.reservationdate);
                    $("#rezervace_datum").val(sel_unit.dataset.reservationdate);
                    var minutes = e.target.dataset.reservationminutes;
                    $("#rezervace_od_txt").val(getTimeString((sel_unit.dataset.reservationfrom)));
                    $("#rezervace_od").val(sel_unit.dataset.reservationfrom);
                    $("#sportoviste_misto").val(misto);
                    $("#rezervace_id").val(sel_unit.dataset.reservationid);
                    $("#zakaznik").val(sel_unit.dataset.reservationuser);
                    $("#stav").val(sel_unit.dataset.reservationstate);
                    $("#cena_interval").val(sportoviste.cena_interval);
                    $("#reservation-modal").modal();

                    $("#rezervace_do")
                            .find("option")
                            .remove();

                    for (var i=1; i<8; i++) {

                        var new_min = parseInt(sel_unit.dataset.reservationfrom) + i* sportoviste.interval_vypujcek;

                        $("#rezervace_do")
                            .append($("<option></option>")
                            .attr("value", new_min)
                            .text(getTimeString(new_min)));


                    }

                    $("#rezervace_do").val(sel_unit.dataset.reservationto);


                    calculatePrice();
                }

            })

            for (var i=0; i< data.result_mista.length; i++) {
               for (var j=0; j<data.result_mista[i].rezervace.length; j++) {
                   var rezervace = data.result_mista[i].rezervace[j];
                   var time_minutes = sportoviste.zacatek_provozu + (j * sportoviste.interval_vypujcek);
                   var num_intervals = (rezervace.rezervace_do_alt - rezervace.rezervace_od_alt) / sportoviste.interval_vypujcek;

                   var klass;

                   if (is_admin) {
                       switch (rezervace.stav) {
                           case 0:
                           {
                               klass = "reservation-reserved";
                               break;
                           }
                           case 1:
                           {
                               klass = "reservation-working";
                               break;
                           }
                           case 2:
                           {
                               klass = "reservation-paid";
                               break;
                           }
                           case 3:
                           {
                               klass = "reservation-pass";
                               break;
                           }
                       }
                   }
                   else {
                       if (rezervace.is_my) {
                           klass = "reservation-myreservation";
                       }
                       else {
                           klass = "reservation-reserved";
                       }

                   }


                   for(var k=0; k<num_intervals; k++) {
                       //console.log(rezervace.rezervace_od_alt + k * sportoviste.interval_vypujcek);
                       var unit = $("#unit_"+data.result_mista[i].id+"_"+(rezervace.rezervace_od_alt + k * sportoviste.interval_vypujcek));
                        unit.addClass(klass);
                           unit.attr('data-reservationid', rezervace.id);
                           unit.attr('data-reservationfrom', rezervace.rezervace_od_alt);
                           unit.attr('data-reservationto', rezervace.rezervace_do_alt);
                           unit.attr('data-reservationuser', rezervace.zakaznik_id);
                           unit.attr('data-reservationstate', rezervace.stav);
                           unit.attr('data-reservationminutes', rezervace.rezervace_do_alt - rezervace.rezervace_od_alt);
                           unit.attr('data-reservationdate', rezervace.rezervace_datum);
                   }

                   calculatePrice();
                }

            }
        });

}

function calculatePrice() {
    var from = parseInt($("#rezervace_od").val());
    var to = parseInt($("#rezervace_do").val());
    var cena_interval = parseFloat($("#cena_interval").val());
    var interval = parseInt($("#interval").val());

    var txt = (((to - from) / interval) * cena_interval) + "Kč";
    $("#cena").html(txt);


}

function getTimeString(minutes) {
    return (minutes % 60 < 10) ? Math.floor(minutes/60) + ":0" + minutes % 60 : Math.floor(minutes/60) + ":" + minutes % 60;
}

