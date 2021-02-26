import gamelib
import tetris
import partida
ALTO_TABLERO,ANCHO_TABLERO=630,350
LONGITUD_CUADRADO=35
def dibujar_superficie(juego):
    game=juego[0]
    for f in range(0,tetris.ALTO_JUEGO):
        for c in range(0,tetris.ANCHO_JUEGO):
            if game[f][c]==1:
                gamelib.draw_rectangle(c*35,f*35,(c*35)+35,(f*35)+35,fill='blue',outline='white') 
def dibujar_piezas(juego):
    _,pieza,pieza_siguiente,_=juego
    graficar_pieza(pieza)
    graficar_pieza(pieza_siguiente)
def graficar_pieza(pieza):
    for posicion in pieza:
        x,y=posicion
        gamelib.draw_rectangle(x*35,y*35,(x*35)+35,(y*35)+35,fill='red',outline='white')
def dibujar_tablero(juego):
    _,_,_,puntuacion=juego
    for f in range(0,ALTO_TABLERO,LONGITUD_CUADRADO):
            for i in range(0,ANCHO_TABLERO,LONGITUD_CUADRADO):
                gamelib.draw_rectangle(i,f,i+LONGITUD_CUADRADO,f+LONGITUD_CUADRADO,fill='black',outline='white')
    gamelib.draw_text('SIGUIENTE PIEZA  ',480,140, fill='white', anchor='nw')
    gamelib.draw_rectangle(455,175,630,400,fill='black',outline='white')
    gamelib.draw_text('Puntuacion: '+str(puntuacion), 400,600, fill='red', anchor='nw')
def dibujar_puntuaciones():
    gamelib.resize(675, 630)
    gamelib.draw_begin
    with open('puntuaciones.txt') as archivo:
        gamelib.draw_rectangle(0,0,675,630,outline='white',fill='black')
        gamelib.draw_text('Puntuaciones',338,10)
        gamelib.draw_rectangle(200,20,500,600,outline='white',fill='black')
        x=55
        for puntuacion in archivo:
            nombre,puntos=puntuacion.rstrip('/n').split(',')
            gamelib.draw_text(nombre+' con '+ puntos,338,x)
            x=x+55
    gamelib.draw_end
    gamelib.wait(gamelib.EventType.KeyPress)