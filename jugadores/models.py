from django.db import models

class Jugador(models.Model):

	id_jug = models.CharField(max_length=50)

	nombre =  models.CharField(max_length=50)

	club = models.CharField(max_length=50)

	edad = models.CharField(max_length=3)

	altura = models.CharField(max_length=10)

	valor = models.IntegerField()

	goles = models.IntegerField()

	asistencias = models.IntegerField()

	amarillas = models.IntegerField()

	segundas_amarillas = models.IntegerField()

	rojas = models.IntegerField()

	tiempo_juego = models.IntegerField()

	victorias = models.IntegerField()

	derrotas = models.IntegerField()

	empates = models.IntegerField()

	ausencias = models.IntegerField()

	foto = models.TextField()

	id_jug = models.CharField(max_length=50)

	def __str__(self):
		return self.nombre
