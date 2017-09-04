from django.db import models

# Create your models here.

class Car(models.Model):
	disponibility = models.BooleanField()

	def __str__(self):
		return str(self.id)