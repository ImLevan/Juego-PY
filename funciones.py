from configuracion import *
import random
import math
import unicodedata
import re

def lectura(archivo, letra, artistaYcancion): #se queda solo con los oraciones de cierta longitud y filtra tildes por ej
    lista = archivo.readlines()
    artistaYcancion=filtrarArtista((lista[0]),artistaYcancion)
    for i in range(1,len(lista)):
        lista[i]=filtrarLinea(filtrarLetras(lista[i]),letra)
        letra.append(lista[i])


def filtrarLetras(cadena): #Reemplaza las tildes y elimina caracteres especiales
    cadena=cadena.lower()
    cadena=re.sub("[-()\n]","",cadena)
    cadena=cadena.replace("á","a")
    cadena=cadena.replace("é","e")
    cadena=cadena.replace("í","i")
    cadena=cadena.replace("ó","o")
    cadena=cadena.replace("ú","u")
    return cadena

def filtrarArtista(linea,artistaYcancion): #Toma la primera linea y seprara los elementos
    elemento=""
    linea=filtrarLetras(linea)
    for caracter in linea+";":
        if caracter==";":
            artistaYcancion.append(elemento)
            elemento=""
        else:
            elemento+=caracter


def filtrarLinea(linea,letra): #Verifica la logitud de las lineas
    candidato=""
    linea=filtrarLetras(linea)
    unaSolaLinea=True #Se asegura que solo haga el proceso una vez
    if len(linea)>60: #Si es muy larga, convierte 1 linea en 2
        mitadDeLinea=len(linea)//2
        for caracter in linea:
            if caracter==" " and len(linea)>mitadDeLinea and unaSolaLinea:
                letra.append(candidato)
                candidato=""
                unaSolaLinea=False
            else:
                candidato+=caracter
    else: #Sino la deja como esta
        candidato=linea
    return candidato

def seleccion(letra):#elige uno al azar, devuelve ese y el siguiente
    posicion=random.randint(0,len(letra)-2)
    linea1=(letra[posicion])
    linea2=(letra[posicion+1])
    return [linea1,linea2]

def puntos(n):#devuelve el puntaje, segun seguidilla
    pts=0
    if n>=1:
        pts=3
    else:
        pts=-3
    return pts

def esCorrecta(palabraUsuario, artistaYcancion, correctas):
    #chequea que sea correcta, que pertenece solo a la frase siguiente. Devuelve puntaje segun seguidilla
    cont=0
    seguidilla=0
    for elemento in artistaYcancion:
        if elemento in palabraUsuario:
            cont=1
    seguidilla=puntos(cont)
    if correctas>=2 and seguidilla>0:
        seguidilla+=50
    return seguidilla