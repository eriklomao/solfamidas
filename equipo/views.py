from bs4 import BeautifulSoup as soup
import requests

from django.shortcuts import render, redirect
from jugadores.models import Jugador
from equipo.models import Equipo
from partidos.models import Partido

from django.contrib import messages

listaInfoPartidos = []
lista_jugadores = []

'''Vista que imprime la pagina del equipo del usuario que este conectado en el momento'''

def equipo(request):

	#Si el usuario logeado no tiene un equipo creado en base de datos redirigir a la web de creación de equipo

	userN = None

	if not request.user.is_authenticated:
		messages.warning(request, 'No puedes acceder a esa seccion sin loguearte')
		return redirect('principal')


	if request.user.is_authenticated:
		userN = request.user.username

	if not Equipo.objects.filter(usuario=userN):
		return render(request, "crear_equipo.html", {})

	#Obtenemos el equipo del usuario conectado y convertimos el string de jugadores en un array

	equipo = Equipo.objects.filter(usuario=request.user.username).all()[0]
	
	a = Equipo.objects.filter(nombre=equipo).values_list('nombre','presupuesto','jugadores')[0]

	if(a[2] is None):
		tempList = []

	else:

		tempList = a[2].split(",")
		
		for i in range(0,len(tempList)):
				tempList[i] = tempList[i].replace('[', '')
				tempList[i] = tempList[i].replace(']', '')
				tempList[i] = tempList[i].strip('\' ')

	b = []
	c= []

	res = ""

	semana = rendimientoSemanal(tempList)

	for jugadores in tempList:
		b.append(Jugador.objects.filter(nombre=jugadores).values_list('nombre','club','edad','altura','valor')[0])
		c.append(Jugador.objects.filter(nombre=jugadores).values_list('nombre','foto','goles','asistencias','amarillas','segundas_amarillas','rojas','tiempo_juego','victorias','derrotas','empates','ausencias')[0])

	res = "|".join(map(str, c))

	#Le pasamos a la plantilla La lista de jugadores la informacion del equipo y los datos de cada jugador.

	return render(request, "equipo.html", {'jugadores': b, 'equipo': a,'datos': res, 'semana': semana})


'''Vista para añadir un jugador nuevo al equipo, el usuario busca un jugador y los datos provenientes de TransferMarkt con respecto
a su busqueda son mostrados'''

def addJugador(request):


	if not request.user.is_authenticated:
		messages.warning(request, 'No puedes acceder a esa seccion sin loguearte')
		return redirect('principal')



	equipo = Equipo.objects.filter(usuario=request.user.username).all()[0]
	
	a = Equipo.objects.filter(nombre=equipo).values_list('nombre','presupuesto','jugadores')[0]

	if(a[2] is None):
		tempList = []

	else:

		tempList = a[2].split(",")
		
		for i in range(0,len(tempList)):
				tempList[i] = tempList[i].replace('[', '')
				tempList[i] = tempList[i].replace(']', '')
				tempList[i] = tempList[i].strip('\' ')



	if len(tempList) == 11:
		messages.warning(request, 'Ya tienes el numero maximo de jugadores, vende alguno antes de comprar')
		return redirect('equipo')


	headers = {'User-Agent':
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

	sid = request.GET.get('search')

	#Cargamos la lista de jugadores resultado de la busqueda del usuario

	global lista_jugadores

	lista_jugadores = []
	temp = []

	if sid == None:
		sid = ""
		lista_jugadores = []
	
	else:
		page = "https://www.transfermarkt.es/schnellsuche/ergebnis/schnellsuche?query=" + sid + "&x=0&y=0"
		pageTree = requests.get(page, headers=headers)
		pageSoup = soup(pageTree.content, 'html.parser')

		Ids = []

		Names = pageSoup.find_all("a", {"class": "spielprofil_tooltip"})

		Position = pageSoup.find_all("td", {"class": "zentriert"})

		Clubs = pageSoup.find_all("a", {"class": "vereinprofil_tooltip"})

		Values = pageSoup.find_all("td", {"class": "rechts hauptlink"})


		for tag in pageSoup.find_all("a", {"class": "spielprofil_tooltip"}):
			Ids.append(tag.get('id'))

		Clubs = Clubs[0::2]
		Position = Position[0::4]

		for i in range(0, len(Names)):
			temp.append(Names[i].text)
			temp.append(Position[i].text)
			temp.append(Values[i].text)
			if (len(Clubs) > i):
				temp.append(Clubs[i].text)
			else:
				temp.append("Sin club")
			temp.append(Ids[i])

			lista_jugadores.append(temp)
			temp = []

	#Cargamos la plantilla a la cual le pasamos el id de los jugadores y la lista de resultados

	return render(request, "anadir.html", {'sid': sid, 'lista_jugadores': lista_jugadores})

'''Añadimos el jugador que el usuario ha seleccionado y actualizamos en base de datos'''

def addPlayer(request):

	if not request.user.is_authenticated:
		messages.warning(request, 'No puedes acceder a esa seccion sin loguearte')
		return redirect('principal')


	id_jug = request.GET.get('add')

	a = Jugador.objects.filter(id_jug=id_jug).all()

	if len(a) >= 1:
		messages.warning(request, 'Ese jugador ya pertenece a un equipo')
		return redirect('addJugador')


	equipo = Equipo.objects.filter(usuario=request.user.username).all()[0]

	headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

	global listaInfoPartidos

	listaInfoPartidos = []

	jugador = {}

	pageInfo = "https://www.transfermarkt.es/lionel-messi/profil/spieler/" + id_jug
	infoTree = requests.get(pageInfo, headers=headers)
	infoSoup = soup(infoTree.content, 'html.parser')

	gdp = infoSoup.find_all("table", {"class": "auflistung"})

	# Primera tabla de la web
	table1 = gdp[0]

	# Hallamos todos los tr
	body = table1.find_all("tr")

	for jugadorIndv in lista_jugadores:
		if jugadorIndv[4] == id_jug:
			jugador["id_jug"] = jugadorIndv[4]
			jugador["nombre"] = jugadorIndv[0]
			jugador["club"] = jugadorIndv[3]
			if len(body[3].td.text) <= 3:
				jugador["edad"] = body[3].td.text
				jugador["altura"] = body[4].td.text
			else:
				jugador["edad"] = body[4].td.text
				jugador["altura"] = body[5].td.text
			jugador["valor"] = jugadorIndv[2]
			jugador["foto"] = ""
			break


	#Scrapeamos todos los datos del jugador y de sus partidos

	pagePartidos = "https://www.transfermarkt.es/x/leistungsdaten/spieler/" + id_jug

	treePartidos = requests.get(pagePartidos, headers=headers)

	soupPartidos = soup(treePartidos.content, 'html.parser')

	listaPartidos = []

	partidoInfo = []

	league = ''

	divFoto = soupPartidos.findAll("div", {"class": "dataBild"})

	srcFoto = divFoto[0].find('img').attrs['src']

	for divs in soupPartidos.findAll("div", {"class": "box"}):

		if len(divs.findAll("a", {
			"name": ["ES1", "IT1", "GB1", "L1", "FR1", "PO1", "RU1", "BE1", "NL1", "A1", "SC1", "UKR1"]})) != 0:
			league = divs

	if (league == ''):
		messages.warning(request, 'Ese jugador no pertenece a las grandes ligas europeas')
		return redirect('addJugador')


	else:

		tablaPartidos = league.find("tbody")

		for partido in tablaPartidos.findAll("tr"):
			listaPartidos.append(partido)

		i = 0

		for j in range(len(listaPartidos)):

			for infoPartido in listaPartidos[j].findAll("td"):

				if i == 0:
					partidoInfo.append(infoPartido.find("a").text.strip())

				elif i == 1:
					partidoInfo.append(infoPartido.text)

				elif i == 2:
					if (infoPartido.text == 'H'):
						partidoInfo.append('Casa')
					elif (infoPartido.text == 'A'):
						partidoInfo.append('Fuera')

				elif i == 3:
					partidoInfo.append(infoPartido.find("img")['alt'])

				elif i == 5:
					partidoInfo.append(infoPartido.find("img")['alt'])

				elif i == 7:
					partidoInfo.append(infoPartido.text.strip())

				elif i == 8:
					if (len(infoPartido.text) > 5):
						partidoInfo.append(infoPartido.text.strip())
						continue
					else:
						partidoInfo.append(infoPartido.find("a")['title'])

				elif i == 9:
					if (infoPartido.text == ''):
						partidoInfo.append('0')
					else:
						partidoInfo.append(infoPartido.text)

				elif i == 10:
					if (infoPartido.text == ''):
						partidoInfo.append('0')
					else:
						partidoInfo.append(infoPartido.text)

				elif i == 11:
					if (infoPartido.text == ''):
						partidoInfo.append('0')
					else:
						partidoInfo.append('1')

				elif i == 12:
					if (infoPartido.text == ''):
						partidoInfo.append('0')
					else:
						partidoInfo.append('1')

				elif i == 13:
					if (infoPartido.text == ''):
						partidoInfo.append('0')
					else:
						partidoInfo.append('1')

				elif i == 14:
					partidoInfo.append(infoPartido.text.strip("'"))

				i += 1

			listaInfoPartidos.append(partidoInfo)
			i = 0
			partidoInfo = []

		jugador["valor"] = int(jugador["valor"].split(",")[0]) * 1000000

		jugador["foto"] = srcFoto

		#Añadimos a la base de datos el jugador

		jugadoresDB(request, equipo, jugador)


	#Redirigimos a la web del equipo

	return redirect('equipo')



#Funcion auxiliar para añadir un jugador a la base de datos

def jugadoresDB(request, equipo, jugador):

	#Contadores para los datos del jugador

	jugador["goles"] = 0
	jugador["asistencias"] = 0
	jugador["amarillas"] = 0
	jugador["segundas_amarillas"] = 0
	jugador["rojas"] = 0
	jugador["tiempo_juego"] = 0
	jugador["victorias"] = 0
	jugador["derrotas"] = 0
	jugador["empates"] = 0
	jugador["ausencias"] = 0

	tempPres = 0

	e = Equipo.objects.get(nombre=equipo)
	tempPres = e.presupuesto - jugador["valor"]

	if tempPres < 0:
		messages.warning(request, 'No tienes fondos suficientes para comprar ese jugador')
		return redirect('addJugador')

		
	if e.jugadores is None:
		tempList = []

	else:

		tempList = e.jugadores.split(",")
		
		for i in range(0,len(tempList)):
				tempList[i] = tempList[i].replace('[', '')
				tempList[i] = tempList[i].replace(']', '')
				tempList[i] = tempList[i].strip('\' ')

	tempList.append(jugador["nombre"])

	#Añadimos el nuevo jugador a la base de datos y actualizamos la lista de jugadores del usuario

	Equipo.objects.filter(nombre=equipo).update(presupuesto=tempPres, jugadores=tempList)

	Jugador.objects.filter(nombre=jugador["nombre"]).delete()

	addJugadorDB = Jugador.objects.create(nombre=jugador["nombre"], club=jugador["club"], edad=jugador["edad"], altura=jugador["altura"], valor=jugador["valor"], goles=jugador["goles"], asistencias=jugador["asistencias"], amarillas=jugador["amarillas"],  segundas_amarillas=jugador["segundas_amarillas"], rojas=jugador["rojas"], tiempo_juego=jugador["tiempo_juego"], victorias=jugador["victorias"], derrotas=jugador["derrotas"], empates=jugador["empates"], ausencias=jugador["ausencias"], foto=jugador["foto"])

'''Eliminamos el jugador que el usuario ha seleccionado y actualizamos en base de datos'''

def delJugador(request):


	if not request.user.is_authenticated:
		messages.warning(request, 'No puedes acceder a esa seccion sin loguearte')
		return redirect('principal')

	equipo = Equipo.objects.filter(usuario=request.user.username).all()[0]

	a = Equipo.objects.filter(nombre=equipo).values_list('nombre','presupuesto','jugadores')[0]

	tempList = a[2].split(",")
	
	for i in range(0,len(tempList)):
			tempList[i] = tempList[i].replace('[', '')
			tempList[i] = tempList[i].replace(']', '')
			tempList[i] = tempList[i].strip('\' ')

	b = []
	c= []

	print(tempList)

	for jugadores in tempList:
		b.append(Jugador.objects.filter(nombre=jugadores).values_list('nombre','club','edad','altura','valor')[0])
		c.append(Jugador.objects.filter(nombre=jugadores).values_list('nombre','goles','asistencias','amarillas','segundas_amarillas','rojas','tiempo_juego','victorias','derrotas','empates','ausencias')[0])

	res = ":".join(map(str, c))

	#Pasamos los datos a la plantilla de los jugadores disponibles que tiene el jugador para vender

	return render(request, "vender.html", {'jugadores': b, 'equipo': a,'datos': res})


#Vista que se ejecuta cuando el jugador decide vender uno de sus jugadores

def delPlayer(request):

	if not request.user.is_authenticated:
		messages.warning(request, 'No puedes acceder a esa seccion sin loguearte')
		return redirect('principal')

	nombre = request.GET.get('del')

	equipo = Equipo.objects.filter(usuario=request.user.username).all()[0]

	e = Equipo.objects.get(nombre=equipo)
	j = Jugador.objects.get(nombre=nombre)		

	tempPres = e.presupuesto + j.valor

	tempList = e.jugadores.split(",")
	
	for i in range(0,len(tempList)):
			tempList[i] = tempList[i].replace('[', '')
			tempList[i] = tempList[i].replace(']', '')
			tempList[i] = tempList[i].strip('\' ')

	tempList.remove(nombre)

	if len(tempList) == 0:
		tempList = None

	#Eliminamos el jugador de la lista en base de datos

	Equipo.objects.filter(nombre=equipo).update(presupuesto=tempPres, jugadores=tempList)

	#Redirigimos a la plantilla de equipo

	return redirect('equipo')

#Vista para crear el equipo con el nombre que desee el usuario

def crear_equipo(request):

	if not request.user.is_authenticated:
		messages.warning(request, 'No puedes acceder a esa seccion sin loguearte')
		return redirect('principal')

	team = request.GET.get('team')

	#Creamos el equipo y lo almacenamos en base de datos con el presupuesto estandar

	teamCreate = Equipo.objects.create(nombre=team,presupuesto=300000000,jugadores=None, usuario=request.user.username)

	#Redirigimos a la pagina del equipo

	return redirect('equipo')


def rendimientoSemanal(datos):

	semana = []

	resultado = [0] * 38

	puntos = 0

	for jugador in datos:
		partidos = Partido.objects.filter(jugador=jugador).values_list('jugador','jornada','localizacion','resultado','goles','asistencias','amarillas','segundas_amarillas','rojas','tiempo_juego').order_by('jornada')

		for partido in partidos:
			semana.append(partido)


	for partido in semana:

		if (int(partido[3].split(":")[0]) > int(partido[3].split(":")[1])):
			if (partido[2] == "Fuera"):
				puntos -= 100
			elif (partido[2] == "Casa"):
				puntos += 100
		elif (int(partido[3].split(":")[0]) < int(partido[3].split(":")[1])):
			if (partido[2] == "Fuera"):
				puntos += 100
			elif (partido[2] == "Casa"):
				puntos -= 100
		if (int(partido[3].split(":")[0]) == int(partido[3].split(":")[1])):
			puntos += 50


		if partido[4] == None:
			puntos -= 50

		else:
			puntos += int(partido[4]) * 100

			puntos += int(partido[5]) * 50

			puntos -= int(partido[6]) * 50

			puntos -= int(partido[8]) * 100

			puntos += int(int(partido[9]) * 0.1)


		resultado[partido[1]-1] = resultado[partido[1]-1] + puntos

		puntos = 0

	return resultado

		

	'''


				score_jugador -= jugador['amarillas'] * 50

				score_jugador -= jugador['rojas'] * 100

				score_jugador -= jugador['ausencias'] * 50'''




