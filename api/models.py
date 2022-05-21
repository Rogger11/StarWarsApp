from django.db import models

class Personaje(models.Model):
    nombre = models.CharField(max_length=150)
    
    def __str__(self) -> str:
        return self.nombre
    
class Planeta(models.Model):
    nombre = models.CharField(max_length=150)
    
    def __str__(self) -> str:
        return self.nombre

class Productor(models.Model):
    nombre = models.CharField(max_length=150)
    
    def __str__(self) -> str:
        return self.nombre
    
class Director(models.Model):
    nombre = models.CharField(max_length=150)
    
    def __str__(self) -> str:
        return self.nombre

class Pelicula(models.Model):
    nombre = models.CharField(max_length=150)
    apertura = models.DateTimeField()
    personajes = models.ManyToManyField(Personaje)
    planetas = models.ManyToManyField(Planeta)
    directores = models.ManyToManyField(Director)
    productores = models.ManyToManyField(Productor)
    
    def __str__(self) -> str:
        return self.nombre