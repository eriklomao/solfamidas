 window.onload = function(){



}

function miFuncion(x){

    // Get the modal
    var modal = document.getElementById("myModal");

    var span = document.getElementsByClassName("close")[0];

    var id = x.getElementsByTagName("td")[4].innerText;

    var sep = x.getElementsByTagName("td")[2].innerText.split(" ");

    var numero = sep[0].split(",")

    var valor = ""

    if(sep[1] == "mill."){
    	valor = "millones de"
    }
    else{
    	valor = "mil"
    }

    document.getElementById("add_si").value = id
    document.getElementById("modal_h3").innerText = "¿Comprar a " + x.getElementsByTagName("td")[0].innerText + "?";
    document.getElementById("modal_p").innerText = "Costara " + numero[0] + " " + valor + " euros de tu presupuesto"

  
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

