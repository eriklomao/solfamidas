var nombres = [];
var goles = [];
var asistencias = [];
var amarillas = [];
var segundas_amarillas = [];
var rojas = [];
var minutos = [];
var victorias = [];
var derrotas = [];
var empates = [];
var ausencias = [];

var myChart;

window.onload = function(){

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

    for(var i = 0;i < datos.length;i++){

        nombres.push(datos[i][0]);
        goles.push(datos[i][2]);
        asistencias.push(datos[i][3]);
        amarillas.push(datos[i][4]);
        segundas_amarillas.push(datos[i][5]);
        rojas.push(datos[i][6]);
        minutos.push(datos[i][7]);
        victorias.push(datos[i][8]);
        derrotas.push(datos[i][9]);
        empates.push(datos[i][10]);
        ausencias.push(datos[i][11]);

        
    }

    var ctx = document.getElementById('myChart').getContext('2d');

    myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: nombres,
        datasets: [{
            label: 'Goles',
            data: goles,
            backgroundColor: [
                    'rgba(235, 59, 90,1.0)',
                    'rgba(250, 130, 49,1.0)',
                    'rgba(247, 183, 49,1.0)',
                    'rgba(32, 191, 107,1.0)',
                    'rgba(15, 185, 177,1.0)',
                    'rgba(69, 170, 242,1.0)',
                    'rgba(75, 123, 236,1.0)',
                    'rgba(165, 94, 234,1.0)',
                    'rgba(209, 216, 224,1.0)',
                    'rgba(119, 140, 163,1.0)',
                    'rgba(253, 121, 168,1.0)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
    });

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

function cambiarGrafico(x){


    var select = document.getElementById("options").value;

    tag = ''

    opcion = []

    switch (select) {
      case "goles":
        tag = "Goles"
        opcion = goles;
        break;
      case "asistencias":
        tag = "Asistencias"      
        opcion = asistencias;
        break;
      case "tarjetas":
        tag = "Tarjetas"
        for(var i = 0;i < amarillas.length;i++){

            opcion.push([amarillas[i], segundas_amarillas[i], rojas[i]])

            
        }
        break;
      case "resultados":
        tag = "Resultados"
        for(var i = 0;i < amarillas.length;i++){

            opcion.push([victorias[i], empates[i], derrotas[i]])
  
        }
        break;
      case "minutos":
        tag = "Minutos"
        opcion = minutos;
        break;
      case "ausencias":
        tag = "Ausencias"
        opcion = ausencias;
        break;
      default:
        //Declaraciones ejecutadas cuando ninguno de los valores coincide con el valor de la expresión
        break;
    }

    var ctx = document.getElementById('myChart').getContext('2d');

    myChart.destroy();

    console.log(tag)

    if(tag == "Tarjetas"){

        myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: nombres,
            datasets: [{

                label: "Amarillas",
                data: amarillas,
                backgroundColor:'rgba(255, 211, 42,1)',
                borderColor:'rgba(255, 211, 42,1.0)',
                

            },

            {

                label: "Segundas Amarillas",
                data: segundas_amarillas,
                backgroundColor:'rgba(240, 147, 43,1.0)',
                borderColor:'rgba(255, 168, 1,1.0)',
                

            },

            {

                label: "Rojas",
                data: rojas,
                backgroundColor:'rgba(255, 63, 52,1)',
                borderColor:'rgba(255, 63, 52,1.0)',
                

            }

            ]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
        });






    }
    else if(tag == "Resultados"){


        myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: nombres,
            datasets: [{

                label: "Victorias",
                data: victorias,
                backgroundColor:'rgba(106, 176, 76,1.0)',
                

            },

            {

                label: "Empates",
                data: empates,
                backgroundColor:'rgba(104, 109, 224,1.0)',
                

            },

            {

                label: "Derrotas",
                data: derrotas,
                backgroundColor:'rgba(255, 63, 52,1.0)',
                

            }

            ]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
        });







    }
    else{

        myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: nombres,
            datasets: [{
                label: tag,
                data: opcion,
                backgroundColor: [
                    'rgba(235, 59, 90,1.0)',
                    'rgba(250, 130, 49,1.0)',
                    'rgba(247, 183, 49,1.0)',
                    'rgba(32, 191, 107,1.0)',
                    'rgba(15, 185, 177,1.0)',
                    'rgba(69, 170, 242,1.0)',
                    'rgba(75, 123, 236,1.0)',
                    'rgba(165, 94, 234,1.0)',
                    'rgba(209, 216, 224,1.0)',
                    'rgba(119, 140, 163,1.0)',
                    'rgba(253, 121, 168,1.0)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
        });




    }


    myChart.update();


}

