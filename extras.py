import pygame
import os, random, sys, math
from pygame.locals import *
from configuracion import *
from pygame.locals import *
from configuracion import *
from funciones import *

def dameLetraApretada(key):
    if key == K_a:
        return("a")
    elif key == K_b:
        return("b")
    elif key == K_c:
        return("c")
    elif key == K_d:
        return("d")
    elif key == K_e:
        return("e")
    elif key == K_f:
        return("f")
    elif key == K_g:
        return("g")
    elif key == K_h:
        return("h")
    elif key == K_i:
        return("i")
    elif key == K_j:
        return("j")
    elif key == K_k:
        return("k")
    elif key == K_l:
        return("l")
    elif key == K_m:
        return("m")
    elif key == K_n:
        return("n")
    elif key == K_o:
        return("o")
    elif key == K_p:
        return("p")
    elif key == K_q:
        return("q")
    elif key == K_r:
        return("r")
    elif key == K_s:
        return("s")
    elif key == K_t:
        return("t")
    elif key == K_u:
        return("u")
    elif key == K_v:
        return("v")
    elif key == K_w:
        return("w")
    elif key == K_x:
        return("x")
    elif key == K_y:
        return("y")
    elif key == K_z:
        return("z")
    elif key == K_KP_MINUS:
        return("-")
    elif key == K_SPACE:
       return(" ")
    elif key == 241:
        return("ñ")
    elif key == K_0:
        return("0")
    elif key == K_1:
        return("1")
    elif key == K_2:
        return("2")
    elif key == K_3:
        return("3")
    elif key == K_4:
        return("4")
    elif key == K_5:
        return("5")
    elif key == K_6:
        return("6")
    elif key == K_7:
        return("7")
    elif key == K_8:
        return("8")
    elif key == K_9:
        return("9")
    else:
        return("")

def main(segundos_menu):

        #Musica
        musica_fondo_path = os.path.join("sonidos", "musica-fondo.mp3")
        musica_fondo=pygame.mixer.music.load(musica_fondo_path)
        musica_fondo=pygame.mixer.music.play(-1)
        musica_fondo=pygame.mixer.music.set_volume(0.3)
        #Centrar la ventana y despues inicializar pygame
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()

        #Preparar la ventana
        pygame.display.set_caption("Cancionero...")
        screen = pygame.display.set_mode((ANCHO, ALTO))
        #definimos funciones
        sonido_correc_path = os.path.join("sonidos", "correcta.ogg")
        sonido_correc=pygame.mixer.Sound(sonido_correc_path)

        sonido_bonus_path = os.path.join("sonidos", "bonus.ogg")
        sonido_bonus=pygame.mixer.Sound(sonido_bonus_path)

        sonido_error_path = os.path.join("sonidos", "Error.ogg")
        sonido_error=pygame.mixer.Sound(sonido_error_path)
        fondo_path = os.path.join("imagenes", "render.jpg")
        fondo = pygame.image.load(fondo_path).convert()
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
        
        archivo_path = os.path.join("letras", str(azar) + ".txt")
        archivo = open(archivo_path, "r", encoding='utf-8') # abre el archivo elegido con unicode.


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



                        archivo_path = os.path.join("letras", str(azar) + ".txt")
                        archivo = open(archivo_path, "r", encoding='utf-8')
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

def dibujar(screen, palabraUsuario, lista, puntos, segundos, ayuda):
    fondo_path = os.path.join("imagenes", "render.jpg")
    fondo = pygame.image.load(fondo_path).convert()
    screen.blit(fondo,[0,0])

    defaultFont= pygame.font.Font( pygame.font.get_default_font(), TAMANNO_LETRA)
    defaultFontGrande= pygame.font.Font( pygame.font.get_default_font(), TAMANNO_LETRA_GRANDE)

    #Linea Horizontal
    pygame.draw.line(screen, (255,255,255), (0, ALTO-70) , (ANCHO, ALTO-70), 5)
    #muestra la indicacion para escribir
    screen.blit(defaultFont.render("Ingrese cancion o artista: ", 1, COLOR_TEXTO), (90,550))
    #muestra lo que escribe el jugador
    screen.blit(defaultFont.render(palabraUsuario, 1, COLOR_TEXTO), (360, 550))
    #muestra el puntaje
    screen.blit(defaultFont.render("Puntos: " + str(puntos), 1, COLOR_TEXTO), (900, 10))
    #muestra los segundos y puede cambiar de color con el tiempo
    if(segundos<15):
        ren = defaultFont.render("Tiempo: " + str(int(segundos)), 1, COLOR_TIEMPO_FINAL)
    else:
        ren = defaultFont.render("Tiempo: " + str(int(segundos)), 1, COLOR_TEXTO)
    screen.blit(ren, (10, 10))

    #muestra el nombre
    screen.blit(defaultFont.render(ayuda, 1, COLOR_PELI), (ANCHO//2-len(ayuda)*TAMANNO_LETRA//3.5,(TAMANNO_LETRA)))

    #muestra las 2 lineas
    screen.blit(defaultFontGrande.render(lista[0], 1, (249, 231, 159)), (ANCHO//2-len(lista[0])*TAMANNO_LETRA_GRANDE//4,(TAMANNO_LETRA_GRANDE)*5))
    screen.blit(defaultFontGrande.render(lista[1], 1, (249, 231, 159)), (ANCHO//2-len(lista[1])*TAMANNO_LETRA_GRANDE//4,(TAMANNO_LETRA_GRANDE)*7))

def draw_text(text,font,color,surface,x,y):
    textObj=font.render(text,1,color)
    textRect=textObj.get_rect()
    textRect.topleft=(x,y)
    surface.blit(textObj,textRect)

mainClock=pygame.time.Clock()
screen = pygame.display.set_mode((ANCHO, ALTO))
def menu():
    font=pygame.font.SysFont(None,20)
    click=False

    tiempo_menu=pygame.time.Clock()
    segundos_menu=0
    segundos=0
    fuente=pygame.font.SysFont("",50)
    fondo_path = os.path.join("imagenes", "render.jpg")
    fondo = pygame.image.load(fondo_path).convert()
    texto1=fuente.render("JUGAR",True,(249, 231, 159))
    texto2=fuente.render("REGLAS",True,(249, 231, 159))
    texto3=pygame.font.Font( pygame.font.get_default_font(), TAMANNO_LETRA).render("Bienvenido al CANCIONERO",1,COLOR_TEXTO)
    texto4=fuente.render("SALIR",True,(249, 231, 159))
    while True:
        screen.fill((0,0,0))
        draw_text("menu",font,(255,255,255),screen,20,20)

        mx,my=pygame.mouse.get_pos()

        button_1=pygame.Rect(450,170,200,50)
        button_2=pygame.Rect(415,270,200,50)
        button_3=pygame.Rect(380,370,200,50)
        if button_1.collidepoint((mx,my)):
            if click:
                segundos_menu=pygame.time.get_ticks()/1000
                main(segundos_menu)
        if button_2.collidepoint((mx,my)):
            if click:
                reglas()
        if button_3.collidepoint((mx,my)):
            if click:
                pygame.quit()
                sys.exit()

        click=False
        pygame.init()
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            if event.type==KEYDOWN:
                if event.key==K_ESCAPE:
                    pygame.quit
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button==1:
                    click=True
        fondo_path = os.path.join("imagenes", "render.jpg")
        fondo = pygame.image.load(fondo_path).convert()
        screen.blit(fondo,[0,0])
        screen.blit(texto1,(450,170))
        screen.blit(texto2,(440,270))
        screen.blit(texto3,(ANCHO//2-23*TAMANNO_LETRA//3.5,(TAMANNO_LETRA)))
        screen.blit(texto4,(460,370))
        pygame.display.update()
        mainClock.tick(60)
        

def reglas():
    fuente=pygame.font.SysFont("",50)
    texto5=fuente.render("VOLVER",True,(0,0,0))
    font=pygame.font.SysFont(None,20)
    click=False
    running=True
    while running:
        screen.fill((0,0,0))

        draw_text("reglas",font,(255,255,255),screen,20,20)
        mx,my=pygame.mouse.get_pos()

        button_5=pygame.Rect(10,10,200,50)

        if button_5.collidepoint((mx,my)):
            if click:
                running=False

        click=False
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            if event.type==KEYDOWN:
                if event.key==K_ESCAPE:
                    running=False
            if event.type == MOUSEBUTTONDOWN:
                if event.button==1:
                    click=True       


        fondo_path = os.path.join("imagenes", "rule.png")
        fondo = pygame.image.load(fondo_path).convert()
        screen.blit(fondo,[0,0])
        screen.blit(texto5,(10,10))
        pygame.display.update()
        mainClock.tick(60)

def finalScene(puntos):
    fuente=pygame.font.SysFont("",50)
    font=pygame.font.SysFont(None,20)
    musica_fondo_path = os.path.join("sonidos", "gameover.mp3")
    musica_fondo=pygame.mixer.music.load(musica_fondo_path)
    musica_fondo=pygame.mixer.music.play(1)
    musica_fondo=pygame.mixer.music.set_volume(0.3)
    defaultFont= pygame.font.Font( pygame.font.get_default_font(), TAMANNO_LETRA)
    texto6=(pygame.font.SysFont("",30)).render("TU PUNTUACION FUE DE: " + str(puntos),1,(255,255,255))
    click=False
    running=True
    while running:
        screen.fill((0,0,0))

        draw_text("finalScene",font,(255,255,255),screen,20,20)
        mx,my=pygame.mouse.get_pos()

        button_6=pygame.Rect(455,425,40,40)
        button_7=pygame.Rect(540,425,40,40)

        if button_6.collidepoint((mx,my)):
            if click:
                segundos_menu=pygame.time.get_ticks()/1000
                main(segundos_menu)
        if button_7.collidepoint((mx,my)):
            if click:
                musica_fondo_path = os.path.join("sonidos", "musica-fondo.mp3")
                musica_fondo=pygame.mixer.music.load(musica_fondo_path)
                musica_fondo=pygame.mixer.music.play(-1)
                musica_fondo=pygame.mixer.music.set_volume(0.3)
                menu()

        click=False
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            if event.type==KEYDOWN:
                if event.key==K_ESCAPE:
                    pygame.quit
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button==1:
                    click=True       

        fondo_path = os.path.join("imagenes", "render.jpg")
        fondo = pygame.image.load(fondo_path).convert()
        screen.blit(fondo,[0,0])
        screen.blit(texto6,(378,10))
        screen.blit(defaultFont.render("JUGAR DE NUEVO?", 1, (255,255,255)), (420,380))
        screen.blit(defaultFont.render("SI", 1, (255,255,255)), (455,425))
        screen.blit(defaultFont.render("NO", 1, (255,255,255)), (540, 425))
        pygame.display.update()   
