import gamelib
import graficos
from operator import itemgetter
#Puntuaciones
def verificar_puntuacion(puntajes,puntos_obtenidos):
    for _,puntaje_guardado in puntajes:
        if puntos_obtenidos>int(puntaje_guardado):
            return True
    return False

def recuperar_puntuaciones():
    puntajes=[]
    with open('puntuaciones.txt')as archivo:
        for linea in archivo:
            if len(linea)==0:
                return puntajes
            nombre,puntaje= linea.rstrip("\n").split(",")
            puntajes.append((nombre,int(puntaje)))
    return puntajes

def comprobar_puntos_obtenidos(puntos_obtenidos):
    puntajes=recuperar_puntuaciones()
    if (len(puntajes)<10 or verificar_puntuacion(puntajes,puntos_obtenidos)):
        gamelib.say('Califico dentro del top 10')
        jugador=gamelib.input(' Ingrese su nombre: ')
        if jugador==None:
            jugador='Jugador'
        puntajes.append((jugador,puntos_obtenidos))
        puntajes=sorted(puntajes,key=lambda x: x[1],reverse=True)
        guardar_puntuacion(puntajes)
    
def guardar_puntuacion(puntos_tabla):
    with open('puntuaciones.txt','w') as archivo_puntuaciones:
        if len(puntos_tabla)>10:
            puntos_tabla=puntos_tabla[:10]
        for nombre,puntos in puntos_tabla:
            archivo_puntuaciones.write("{},{}\n".format(nombre,puntos))
#Partida
def guardar_partida(juego):
    tablero,pieza_actual,nueva_pieza,puntuacion=juego
    with open('partida.txt','w') as archivo_partida:
        archivo_partida.write(desarmar_pieza(pieza_actual)+"\n")
        archivo_partida.write(desarmar_pieza(nueva_pieza)+"\n")
        archivo_partida.write(str(puntuacion)+"\n")
        for numero_fila,fila in enumerate(tablero):
            if numero_fila==len(tablero):
                archivo_partida.write(str(fila))
            else:
                archivo_partida.write(str(fila)+"\n")

def cargar_partida(ruta_partida):
    juego=[]
    with open(ruta_partida) as archivo_partida:
        pieza_actual=armar_pieza(archivo_partida.readline())
        pieza_siguiente=armar_pieza(archivo_partida.readline())
        puntuacion=int(archivo_partida.readline())
        for linea in archivo_partida:
            linea=linea.rstrip("\n")
            juego.append(transformar_linea(linea))
    return tuple(juego),pieza_actual,pieza_siguiente,puntuacion

def desarmar_pieza(pieza):
    pieza_desarmada=''
    contador_posiciones=0
    for posicion in pieza:
        x,y=posicion
        if contador_posiciones==3:
            pieza_desarmada= pieza_desarmada+str(x)+','+(str(y))
        else:
            pieza_desarmada= pieza_desarmada+str(x)+','+(str(y)+';')
            contador_posiciones=contador_posiciones+1
    return pieza_desarmada

def armar_pieza(pieza):
    pieza_nueva=[]
    pieza=pieza.split(';')
    for posicion in pieza:
        x,y=posicion.split(',')
        pieza_nueva.append(((int(x)),(int(y))))
    return tuple(pieza_nueva)

def transformar_linea(linea):
    fila=[]
    linea=linea.strip('[]')
    valores_fila=linea.split(',')
    for elemento in valores_fila:
        fila.append(int(elemento)) 
    return fila

