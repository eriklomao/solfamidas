 window.onload = function(){



}

function miFuncion(x){

    // Get the modal
    var modal = document.getElementById("myModal");

    var span = document.getElementsByClassName("close")[0];

    var nombre = x.getElementsByTagName("td")[0].innerText;

    var sep = x.getElementsByTagName("td")[4].innerText;

    var numero = parseInt(sep) / 1000000;

    console.log(numero)

    var valor = ""

    if(numero%1 == 0){
    	valor = "millones de"
    }
    else{
        numero = numero * 1000
    	valor = "mil"
    }

    document.getElementById("del_si").value = nombre
    document.getElementById("modal_h3").innerText = "¿Vender a " + x.getElementsByTagName("td")[0].innerText + "?";
    document.getElementById("modal_p").innerText = "Seran devueltos " + numero + " " + valor + " euros a tu presupuesto"

  
    modal.style.display = "block";

    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
        modal.style.display = "none";
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }


}

