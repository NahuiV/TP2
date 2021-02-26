import tetris
import gamelib
import partida
import graficos
ALTO_TABLERO,ANCHO_TABLERO=630,350
LONGITUD_CUADRADO=35
ESPERA_DESCENDER = 8
def cargar_acciones():
    acciones={}
    with open('teclas.txt') as archivo_teclas:
        for linea in archivo_teclas:
            tecla,accion=linea.rstrip().split('=')
            acciones[tecla]=accion
    return acciones

def actualizar_juego(juego,accion,pieza_siguiente,rotaciones):
    if accion=='IZQUIERDA':
        return tetris.mover(juego,tetris.IZQUIERDA)
    elif accion=='DERECHA':
        return tetris.mover(juego,tetris.DERECHA)
    elif accion=='ROTAR':
        return tetris.rotar(juego,rotaciones)
    elif accion=='DESCENDER':
        estado_actual,terminado=tetris.avanzar(juego,pieza_siguiente)
        if not terminado:
            return estado_actual
        partida.comprobar_puntos_obtenidos(estado_actual[3])
        graficos.dibujar_puntuaciones()      
    elif accion=='GUARDAR':
        partida.guardar_partida(juego)
        return juego
    elif accion=='CARGAR':
        return partida.cargar_partida('partida.txt')
    elif accion=='SALIR':
        return  

def main():
    juego=tetris.crear_juego()
    gamelib.resize(675, 630)
    timer_bajar = ESPERA_DESCENDER
    acciones=cargar_acciones()
    rotaciones=tetris.recuperar_piezas()
    while gamelib.loop(fps=30):
        if timer_bajar==ESPERA_DESCENDER:
            siguiente_pieza=juego[2]
        gamelib.draw_begin()
        graficos.dibujar_tablero(juego)
        graficos.dibujar_piezas(juego)
        graficos.dibujar_superficie(juego)
        gamelib.draw_end()
        for event in gamelib.get_events():
          if not event:
              break
          if event.type == gamelib.EventType.KeyPress:
            tecla = event.key
            juego=actualizar_juego(juego,acciones[tecla],siguiente_pieza,rotaciones)
        
        timer_bajar -= 1
        if timer_bajar == 0:
            timer_bajar = ESPERA_DESCENDER
            juego,termino=tetris.avanzar(juego,siguiente_pieza)
            if termino==True:
                partida.comprobar_puntos_obtenidos(juego[3])
                graficos.dibujar_puntuaciones()
                break
gamelib.init(main)