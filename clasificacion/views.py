from django.shortcuts import render

from equipo.models import Equipo

from jugadores.models import Jugador

import numpy as np

'''Vista que calcula e imprime la puntuacion de cada equipo en orden descendente'''

def clasificacion(request):

	score_jugador = 0

	score_equipo = 0

	score_total = []

	equipo_total = []

	usuarios_total = []

	lista_equipos = Equipo.objects.all().values()

	#Calculamos la puntuacion de cada jugador y de los equipos

	for equipo in lista_equipos:

		if equipo['jugadores'] is None:
			score_equipo = 0

		else:

			tempList = equipo['jugadores'].split(",")
		
			for i in range(0,len(tempList)):
					tempList[i] = tempList[i].replace('[', '')
					tempList[i] = tempList[i].replace(']', '')
					tempList[i] = tempList[i].strip('\' ')

			for player in tempList:

				jugador = Jugador.objects.filter(nombre=player).values()[0]

				score_jugador += jugador['victorias'] * 100

				score_jugador += jugador['empates'] * 50

				score_jugador -= jugador['derrotas'] * 100

				score_jugador += jugador['goles'] * 100

				score_jugador += jugador['asistencias'] * 50

				score_jugador += int(jugador['tiempo_juego'] * 0.1)

				score_jugador -= jugador['amarillas'] * 50

				score_jugador -= jugador['rojas'] * 100

				score_jugador -= jugador['ausencias'] * 50

				score_equipo += score_jugador

				score_jugador = 0


		score_total.append([equipo['nombre'],score_equipo,equipo['usuario']])

		score_equipo = 0


	#Ordenamos el resultado mediante Bubble sort
	n = len(score_total)
  
  
	for i in range(n-1):
		for j in range(0, n-i-1):
			if score_total[j][1] < score_total[j+1][1] :
				score_total[j], score_total[j+1] = score_total[j+1], score_total[j]


	#Le pasamos a la plantilla las puntuaciones de cada equipo de forma ordenada

	return render(request, "clasificacion.html", {'scores': score_total})
