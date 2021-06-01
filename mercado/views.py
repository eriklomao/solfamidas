from django.shortcuts import render

from bs4 import BeautifulSoup as soup

import requests

import time

def mercado(request):

	sid = ""
	name = ""

	lista_jugadores = []

	detalles = []

	if request.method == 'POST':

		sid = request.POST.get("search")

		name = request.POST.get("name")

		details = request.POST.get("details")

		print(sid)

		if details != None:
			detalles = detallesJugadores(details)

		
		lista_jugadores	= datosTabla(sid)
		
	return render(request, "Mercado.html", {'sid': sid, 'lista_jugadores': lista_jugadores, 'detalles': detalles, 'name': name})

def datosTabla(sid):

	headers = {'User-Agent':
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

	lista_jugadores = []

	temp = []

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

	return lista_jugadores;


def detallesJugadores(id_jug):

	headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

	listaInfoPartidos = []

	jugador = {}

	#Scrapeamos todos los datos del jugador y de sus partidos

	pagePartidos = "https://www.transfermarkt.es/x/leistungsdaten/spieler/" + id_jug

	treePartidos = requests.get(pagePartidos, headers=headers)

	soupPartidos = soup(treePartidos.content, 'html.parser')

	listaPartidos = []

	partidoInfo = []

	datos = [0,0,0,0,0,0,0,'']

	league = ''

	divFoto = soupPartidos.findAll("div", {"class": "dataBild"})

	srcFoto = divFoto[0].find('img').attrs['src']

	for divs in soupPartidos.findAll("div", {"class": "box"}):

		if len(divs.findAll("a", {
			"name": ["ES1", "IT1", "GB1", "L1", "FR1", "PO1", "RU1", "BE1", "NL1", "A1", "SC1", "UKR1"]})) != 0:
			league = divs

	if (league == ''):
		return "No pertenece"

	else:

		tablaPartidos = league.find("tbody")

		for partido in tablaPartidos.findAll("tr"):
			listaPartidos.append(partido)

		i = 0

		for j in range(len(listaPartidos)):

			for infoPartido in listaPartidos[j].findAll("td"):

				if i == 8:
					if (len(infoPartido.text) > 5):
						datos[6] = datos[6] + 1
						continue
				elif i == 9:
					if (infoPartido.text == ''):
						datos[0] = datos[0] + 0
					else:
						datos[0] = datos[0] + int(infoPartido.text)

				elif i == 10:
					if (infoPartido.text == ''):
						datos[1] = datos[1] + 0
					else:
						datos[1] = datos[1] + int(infoPartido.text)

				elif i == 11:
					if (infoPartido.text == ''):
						datos[2] = datos[2] + 0
					else:
						datos[2] = datos[2] + 1


				elif i == 12:
					if (infoPartido.text == ''):
						datos[3] = datos[3] + 0
					else:
						datos[3] = datos[3] + 1

				elif i == 13:
					if (infoPartido.text == ''):
						datos[4] = datos[4] + 0
					else:
						datos[4] = datos[4] + 1

				elif i == 14:
					datos[5] = datos[5] + int(infoPartido.text.strip("'"))

				i += 1

			i = 0
	
		datos[7] = srcFoto

		return datos




