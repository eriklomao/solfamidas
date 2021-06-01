from django.db import models

class Partido(models.Model):

	jugador = models.CharField(max_length=50)

	jornada =  models.IntegerField()

	fecha = models.CharField(max_length=50)

	localizacion = models.CharField(max_length=50)

	club = models.CharField(max_length=50)

	adversario = models.CharField(max_length=50)

	resultado = models.CharField(max_length=50)

	posicion = models.CharField(max_length=50)

	goles = models.CharField(max_length=50)

	asistencias = models.CharField(max_length=50)

	amarillas = models.CharField(max_length=50)

	segundas_amarillas = models.CharField(max_length=50)

	rojas = models.CharField(max_length=50)

	tiempo_juego = models.CharField(max_length=50)

	def __str__(self):
		return self.jugador
