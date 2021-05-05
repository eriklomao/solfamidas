from djongo import models

class Equipo(models.Model):

	nombre =  models.CharField(max_length=50)

	presupuesto = models.IntegerField()

	jugadores = models.TextField()

	usuario = models.CharField(max_length=50)

	def __str__(self):
		return self.nombre