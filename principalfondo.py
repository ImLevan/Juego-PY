#! /usr/bin/env python
import os, random, sys, math
import pygame
from pygame.locals import *
from configuracion import *
from extras import *
from funciones import *
pygame.init()
pygame.display.set_caption("game base")
screen=pygame.display.set_mode((1024,600),0,32)

musica_fondo=pygame.mixer.music.load(".\\sonidos\\musica-fondo.mp3")
musica_fondo=pygame.mixer.music.play(-1)
musica_fondo=pygame.mixer.music.set_volume(0.3)


#Funcion principal
def main(segundos_menu):

        #Musica
        musica_fondo=pygame.mixer.music.load(".\\sonidos\\musica-fondo.mp3")
        musica_fondo=pygame.mixer.music.play(-1)
        musica_fondo=pygame.mixer.music.set_volume(0.3)
        #Centrar la ventana y despues inicializar pygame
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()

        #Preparar la ventana
        pygame.display.set_caption("Cancionero...")
        screen = pygame.display.set_mode((ANCHO, ALTO))
        #definimos funciones
        sonido_correc=pygame.mixer.Sound(".\\sonidos\\correcta.ogg")

        sonido_bonus=pygame.mixer.Sound(".\\sonidos\\bonus.ogg")

        sonido_error=pygame.mixer.Sound(".\\sonidos\\error.ogg")
        fondo=pygame.image.load("render.jpg").convert()
        screen.blit(fondo,[0,0])
        
        #tiempo total del juego
        gameClock = pygame.time.Clock()
        totaltime = 0
        segundos = TIEMPO_MAX
        fps = FPS_inicial
        artistaYcancion=[]
        puntos = 0
        palabraUsuario = ""
        letra=[]
        correctas=0
        elegidos= []
        masDeUnaVuelta = False
        bonus=False

        #elige una cancion de todas las disponibles
        azar=random.randrange(1,N+1)
        elegidos.append(azar) #la agrega a la lista de los ya elegidos
        archivo= open(".\\letras\\"+str(azar)+".txt","r", encoding='utf-8') # abre el archivo elegido con unicode.


        #lectura del archivo y filtrado de caracteres especiales, la primer linea es el artista y ca
        lectura(archivo, letra, artistaYcancion)


        #elige una linea al azar y su siguiente
        lista=seleccion(letra)

        ayuda = "Cancionero"
        dibujar(screen, palabraUsuario, lista, puntos, segundos, ayuda)

        while segundos > fps/1000:
        # 1 frame cada 1/fps segundos
            gameClock.tick(fps)
            totaltime += gameClock.get_time()
            if True:
             fps = 3

            #Buscar la tecla apretada del modulo de eventos de pygame
            for e in pygame.event.get():



                #QUIT es apretar la X en la ventana
                if e.type == QUIT:
                    pygame.quit()
                    return()


                #Ver si fue apretada alguna tecla
                if e.type == KEYDOWN:
                    letraApretada = dameLetraApretada(e.key)
                    palabraUsuario += letraApretada
                    if e.key == K_BACKSPACE:
                        palabraUsuario = palabraUsuario[0:len(palabraUsuario)-1]
                    if e.key == K_RETURN:
                        #chequea si es correcta y suma o resta puntos
                        sumar=esCorrecta(palabraUsuario, artistaYcancion, correctas)
                        puntos+=sumar
                        ##pygame.mixer.music.play()

                        bonus=False

                        if sumar>0 and sumar<50:
                            correctas=correctas+1
                            sonido_correc.play()

                        elif sumar>50:
                            bonus=True
                            correctas=0
                            sonido_bonus.play()
                        else:
                            correctas=0
                            sonido_error.play()
                        if len(elegidos)==N:
                                elegidos=[]
                                masDeUnaVuelta = True

                        azar=random.randrange(1,N+1)
                        while(azar in elegidos):
                            azar=random.randrange(1,N+1)

                        elegidos.append(azar)

                        if masDeUnaVuelta == True or len(elegidos) >= 2: #despues de la primera canciones tira la ayuda
                            ayuda = "Pista anterior: " + artistaYcancion[0]



                        archivo= open(".\\letras\\"+str(azar)+".txt","r", encoding='utf-8')
                        palabraUsuario = ""
                        #lectura del archivo y filtrado de caracteres especiales
                        artistaYcancion=[]
                        letra = []
                        lectura(archivo, letra, artistaYcancion)

                        #elige una linea al azar y su siguiente
                        lista=seleccion(letra)

            if bonus:
                segundos =TIEMPO_BONUS+segundos_menu+TIEMPO_MAX -pygame.time.get_ticks()/1000

            else:
                segundos =segundos_menu+TIEMPO_MAX -pygame.time.get_ticks()/1000

            #Limpiar pantalla anterior
            screen.fill(COLOR_FONDO)

            #Dibujar de nuevo todo
            dibujar(screen, palabraUsuario, lista, puntos, segundos, ayuda)
            pygame.display.flip()
        
        finalScene(puntos)
        
        while 1:
            #Esperar el QUIT del usuario
            for e in pygame.event.get():
                if e.type == QUIT:
                    pygame.quit()
                    return

        archivo.close()

#Llamada a a pantalla del menu
menu()
#Llamada a la pantalla reglas
reglas()
#Llamada a la pantalla final
finalScene(puntos)



#Programa Principal ejecuta Main
if name == "__main__":
    main()