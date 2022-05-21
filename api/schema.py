import graphene

from graphene_django import DjangoObjectType, DjangoListField 
from .models import * 
from graphene_django.filter import DjangoFilterConnectionField
from graphene import relay


class PeliculaType(DjangoObjectType): 
    class Meta:
        model = Pelicula
        fields = "__all__"
        interfaces = (relay.Node, )
        
        
class PersonajeType(DjangoObjectType):
    class Meta:
        model = Personaje
        fields = "__all__"


class PlanetaType(DjangoObjectType):
    class Meta:
        model = Planeta
        fields = "__all__"


class DirectorType(DjangoObjectType):
    class Meta:
        model = Director
        fields = "__all__"


class ProductorType(DjangoObjectType):
    class Meta:
        model = Productor
        fields = "__all__"


class Query(graphene.ObjectType):
    all_peliculas = graphene.List(PeliculaType)
    personaje = graphene.Field(PeliculaType, nombre=graphene.String())

    def resolve_all_peliculas(self, info, **kwargs):
        return Pelicula.objects.all()

    def resolve_personaje(self, info, nombre):
        if Pelicula.objects.filter(personajes__nombre=nombre):
            pelicula = Pelicula.objects.filter(personajes__nombre=nombre)
            appe = None
            for i in pelicula:
                if appe is None:
                    appe = Pelicula.objects.get(nombre=i.nombre)
            return appe
        else:
            return "Not found"
    
class PersonajeInput(graphene.InputObjectType):
    nombre = graphene.String(required=True)
    
class PlanetaInput(graphene.InputObjectType):
    nombre = graphene.String(required=True)
    
class DirectorInput(graphene.InputObjectType):
    nombre = graphene.String(required=True)
    
class ProductorInput(graphene.InputObjectType):
    nombre = graphene.String(required=True)
    
class PeliculaCrear(graphene.Mutation):
    pelicula = graphene.Field(PeliculaType)
    
    class Arguments:
        nombre = graphene.String(required=True)
        apertura = graphene.DateTime(required=True)
        personajes = graphene.List(PersonajeInput, required=True)
        planetas = graphene.List(PlanetaInput, required=True)
        directores = graphene.List(DirectorInput, required=True)
        productores = graphene.List(ProductorInput, required=True)

    def mutate(self, info, nombre, apertura, personajes, planetas, directores, productores):
        pelicula_instance = Pelicula( 
            nombre=nombre,
            apertura=apertura,
        )
        pelicula_instance.save()
        for i in personajes:
            pelicula_instance.personajes.get_or_create(nombre=i['nombre'])
        for i in planetas:
            pelicula_instance.planetas.get_or_create(nombre=i['nombre'])
        for i in directores:
            pelicula_instance.directores.get_or_create(nombre=i['nombre'])
        for i in productores:
            pelicula_instance.productores.get_or_create(nombre=i['nombre'])
        return PeliculaCrear(pelicula=pelicula_instance)
    
class Mutation(graphene.ObjectType):
    Pelicula_crear = PeliculaCrear.Field()
    
schema = graphene.Schema(query=Query, mutation=Mutation)