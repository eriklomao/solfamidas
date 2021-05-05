window.onload = function(){


}

function miFuncion(x){

    // Get the modal
    var modal = document.getElementById("myModal");

    var span = document.getElementsByClassName("close")[0];

    var datosStr = document.getElementById("myVar").value;

    var datosT = datosStr.split("|")

    var datos = [];

    for(var i = 0;i < datosT.length;i++){

        temp = datosT[i].split(",");

        for(var j = 0;j < 12;j++){

            temp[j] = temp[j].trim()
        }

        temp[0] = temp[0].replaceAll("'", "");
        temp[0] = temp[0].replaceAll("(", "");
        temp[1] = temp[1].replaceAll("'", "");
        temp[11] = temp[11].replaceAll(")", "");

        datos.push(temp);

    }

    var nombreJugador = x.getElementsByTagName("td")[0].innerText

    for(var i = 0;i < datosT.length;i++){

        if(datos[i][0] == nombreJugador){

            var datosJugador = datos[i]
        }

    }


    document.getElementById('jugNombre').innerText = datosJugador[0];
    document.getElementById('jugFoto').src = datosJugador[1];
    document.getElementById('jugGoles').innerText = "Goles: " + datosJugador[2];
    document.getElementById('jugAsist').innerText = "Asistencias: " + datosJugador[3];
    document.getElementById('jugAma').innerText = "Amarillas: " + datosJugador[4];
    document.getElementById('jugSegAma').innerText = "Segundas Amarillas: " + datosJugador[5];
    document.getElementById('jugRojas').innerText = "Rojas: " + datosJugador[6];
    document.getElementById('jugMin').innerText = "Minutos totales de juego: " + datosJugador[7];
    document.getElementById('jugVic').innerText = "Victorias: " + datosJugador[8];
    document.getElementById('jugDer').innerText = "Derrotas: " + datosJugador[9];
    document.getElementById('jugEmp').innerText = "Empates: " + datosJugador[10];
    document.getElementById('jugAus').innerText = "Partidos ausente: " + datosJugador[11];


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

