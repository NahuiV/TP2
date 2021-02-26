ANCHO_JUEGO, ALTO_JUEGO = 10, 18
IZQUIERDA, DERECHA = -1, 1
import random
import gamelib
def generar_pieza():
    """
    Genera una nueva pieza de entre PIEZAS al azar. Si se especifica el parámetro pieza
    se generará una pieza del tipo indicado. Los tipos de pieza posibles
    están dados por las constantes CUBO, Z, S, I, L, L_INV, T.

    El valor retornado es una tupla donde cada elemento es una posición
    ocupada por la pieza, ubicada en (0, 0). Por ejemplo, para la pieza
    I se devolverá: ( (0, 0), (0, 1), (0, 2), (0, 3) ), indicando que 
    ocupa las posiciones (x = 0, y = 0), (x = 0, y = 1), ..., etc.
    """
    piezas=primeras_posiciones()
    posicion=random.randrange(len(piezas))
    pieza=piezas[posicion]
    return pieza   

def trasladar_pieza(pieza, dy, dx):
    """
    Traslada la pieza de su posición actual a (posicion + (dx, dy)).

    La pieza está representada como una tupla de posiciones ocupadas,
    donde cada posición ocupada es una tupla (x, y). 
    Por ejemplo para la pieza ( (0, 0), (0, 1), (0, 2), (0, 3) ) y
    el desplazamiento dx=2, dy=3 se devolverá la pieza 
    ( (2, 3), (2, 4), (2, 5), (2, 6) ).
    """
    pieza_trasladada=[]
    for elemento in pieza:
        xi,yi=elemento
        pieza_trasladada.append(((xi + dy) ,(yi+dx)))
    return tuple(pieza_trasladada)

def crear_juego():
    """
    Crea un nuevo juego de Tetris.

    El parámetro pieza_inicial es una pieza obtenida mediante 
    pieza.generar_pieza. Ver documentación de esa función para más información.

    El juego creado debe cumplir con lo siguiente:
    - La grilla está vacía: hay_superficie da False para todas las ubicaciones
    - La pieza actual está arriba de todo, en el centro de la pantalla.
    - El juego no está terminado: terminado(juego) da False

    Que la pieza actual esté arriba de todo significa que la coordenada Y de 
    sus posiciones superiores es 0 (cero).
    """
    puntuacion=0
    pieza_inicial=generar_pieza()
    siguiente_pieza_cen=trasladar_pieza(generar_pieza(),15,6)
    pieza_centrada=trasladar_pieza(pieza_inicial,ANCHO_JUEGO//2,0)
    grilla=[]
    for _ in range(0,ALTO_JUEGO):
        grilla.append([0]*ANCHO_JUEGO)
    return tuple(grilla),pieza_centrada,siguiente_pieza_cen,puntuacion

def dimensiones(juego):
    """
    Devuelve las dimensiones de la grilla del juego como una tupla (ancho, alto).
    """
    grilla=juego[0]
    return len(grilla[0]),len(grilla)

def pieza_actual(juego):
    """
    Devuelve una tupla de tuplas (x, y) con todas las posiciones de la
    grilla ocupadas por la pieza actual.

    Se entiende por pieza actual a la pieza que está cayendo y todavía no
    fue consolidada con la superficie.

    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    """
    return juego[1]

def hay_superficie(juego, x, y):
    """
    Devuelve True si la celda (x, y) está ocupada por la superficie consolidada.
    
    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    """
    game=juego[0]
    if not(game[y][x]==1):
        return False
    return True

def mover(juego, direccion):
    """
    Mueve la pieza actual hacia la derecha o izquierda, si es posible.
    Devuelve un nuevo estado de juego con la pieza movida o el mismo estado 
    recibido si el movimiento no se puede realizar.

    El parámetro direccion debe ser una de las constantes DERECHA o IZQUIERDA.
    """
    tablero,pieza_actual,pieza_siguiente,puntuacion=juego
    pieza_final=trasladar_pieza(pieza_actual,direccion,0)
    for elemento in pieza_final:
        x_pared,y_pared=elemento
        if (direccion==1 and x_pared>(ANCHO_JUEGO-1)) or(direccion==-1 and x_pared<0) or (hay_superficie(juego,x_pared,y_pared)==True):
                return juego
    
    return tablero,pieza_final,pieza_siguiente,puntuacion

def avanzar(juego,pieza_nueva):
    puntuacion=0
    """
    Avanza al siguiente estado de juego a partir del estado actual.
    
    Devuelve una tupla (juego_nuevo, cambiar_pieza) donde el primer valor
    es el nuevo estado del juego y el segundo valor es un booleano que indica
    si se debe cambiar la siguiente_pieza (es decir, se consolidó la pieza
    actual con la superficie).
    
    Avanzar el estado del juego significa:
     - Descender una posición la pieza actual.
     - Si al descender la pieza no colisiona con la superficie, simplemente
       devolver el nuevo juego con la pieza en la nueva ubicación.
     - En caso contrario, se debe
       - Consolidar la pieza actual con la superficie.
       - Eliminar las líneas que se hayan completado.
       - Cambiar la pieza actual por siguiente_pieza.

    Si se debe agregar una nueva pieza, se utilizará la pieza indicada en
    el parámetro siguiente_pieza. El valor del parámetro es una pieza obtenida 
    llamando a generar_pieza().

    **NOTA:** Hay una simplificación respecto del Tetris real a tener en
    consideración en esta función: la próxima pieza a agregar debe entrar 
    completamente en la grilla para poder seguir jugando, si al intentar 
    incorporar la nueva pieza arriba de todo en el medio de la grilla se
    pisara la superficie, se considerará que el juego está terminado.

    Si el juego está terminado (no se pueden agregar más piezas), la funcion no hace nada, 
    se debe devolver el mismo juego que se recibió.
    """
    tablero,pieza_actual,_,puntuacion_guardada=juego
    if terminado(juego)==True:
        return juego,True
    pieza_trasladada=trasladar_pieza(pieza_actual,0,1)
    if verificar_avance(juego,pieza_trasladada)==True:
        return (tablero,pieza_trasladada,pieza_nueva,puntuacion_guardada+puntuacion),False
    else:
        siguiente_pieza_centrada=trasladar_pieza(pieza_nueva,-15,-6)
        siguiente_pieza_centrada=trasladar_pieza(siguiente_pieza_centrada,ANCHO_JUEGO//2,0)
        grilla=consolidar_pieza(list(tablero),pieza_actual)
        puntuacion=puntuacion_guardada+sumar_puntuacion(5)
        gamelib.play_sound('sound/fall.wav')
        grilla,puntos=borrar_filas(grilla)
        puntuacion+=puntos
        for posicion in siguiente_pieza_centrada:
            x,y=posicion
            if(grilla[x][y]==1):
                return (grilla,siguiente_pieza_centrada,pieza_nueva,puntuacion),True

    return (grilla,siguiente_pieza_centrada,trasladar_pieza(generar_pieza(),15,6),puntuacion),False

def terminado(juego):
    """
    Devuelve True si el juego terminó, es decir no se pueden agregar
    nuevas piezas, o False si se puede seguir jugando.
    """
    game=juego[0]
    pieza_creada=pieza_actual(juego)
    for elemento in pieza_creada:
        x,y=elemento
        if game[y][x]==1:
            return True
    return False

def borrar_filas(juego):
    'Borra las filas donde cada uno de sus elementos sea C. Si se borro alguna fila ,la intercambia con la que tenga almenos una C a partir de la anterior'
    nuevo_juego=[]
    puntos=0
    for fila in range(0,len(juego)):
        if not all(juego[fila]):
            nuevo_juego.append(juego[fila])
    if len(nuevo_juego)!=ALTO_JUEGO:
        cantidad_nuevas_filas=ALTO_JUEGO-len(nuevo_juego)
        puntos=sumar_puntuacion(cantidad_nuevas_filas)
        for _ in range(0,cantidad_nuevas_filas):
            nuevo_juego.insert(0,[0]*ANCHO_JUEGO)
        gamelib.play_sound('sound/line.wav')
    return tuple(nuevo_juego),puntos

def consolidar_pieza(juego,pieza):
    for posicion in pieza:
        x,y=posicion
        juego[y][x]=1
    return tuple(juego)

def verificar_avance(juego,pieza_verificar):
    for posicion in pieza_verificar:
        x,y=posicion
        if y>=(ALTO_JUEGO) or x>=(ANCHO_JUEGO) or hay_superficie(juego,x,y):
            return False
    return True

def rotar(juego,rotaciones):
    tablero,pieza,pieza_siguiente,puntuacion=juego
    pieza_ordenada=tuple(sorted(pieza))
    primer_posicion=pieza_ordenada[0]
    pieza_en_origen=trasladar_pieza(pieza_ordenada,-primer_posicion[0],-primer_posicion[1])
    siguiente_rotacion=rotaciones[pieza_en_origen]
    pieza_nueva=trasladar_pieza(siguiente_rotacion,primer_posicion[0],primer_posicion[1])
    if not verificar_avance(juego,pieza_nueva):
        return tablero,pieza,pieza_siguiente,puntuacion
    return tablero,pieza_nueva,pieza_siguiente,puntuacion

def convertir_str(pieza):
    '''Convierte la pieza que se encuentra en string a una tupla de tuplas que son las posiciones de la pieza'''
    pieza_final=[]
    for posicion_str in pieza:
        posicion_convertida=[]
        lista_posiciones=posicion_str.split(';')
        for posicion in lista_posiciones:
            x,y=posicion.split(',')
            posicion_convertida.append(((int(x)),(int(y))))
        pieza_final.append(tuple(posicion_convertida))
    return tuple(pieza_final)

def sumar_puntuacion(opcion_puntaje):
    '''Devuelve un entero segun la accion que se complete, devuelve una puntuacion segun la cantidad de lineas completas al consolidar una pieza o si consolida una pieza'''
    opciones_puntajes=[(1,100),(2,200),(3,400),(4,800),(5,10)]
    for opcion,puntos in opciones_puntajes:
        if opcion==opcion_puntaje:
            return puntos
    
def primeras_posiciones():
    '''Obtengo las primeras posiciones de cada pieza y las devuelvo una lista con cada una de ellas'''
    piezas=[]
    with open('piezas.txt') as archivo_piezas:
        for linea in archivo_piezas:
            rotaciones_pieza,_=linea.rstrip().split('#')
            rotaciones_pieza=rotaciones_pieza.split(' ')
            rotaciones_pieza=convertir_str(rotaciones_pieza)
            piezas.append(rotaciones_pieza[0])
    return piezas

def recuperar_piezas():
    piezas={}
    with open('piezas.txt') as archivo_piezas:
        for linea in archivo_piezas:
            rotaciones_pieza,_=linea.rstrip().split('#')
            rotaciones_pieza=rotaciones_pieza.split(' ')
            rotaciones_pieza=convertir_str(rotaciones_pieza)
            pieza_nueva=[]
            longitud=len(rotaciones_pieza)
            for rotacion in rotaciones_pieza:
                if rotaciones_pieza.index(rotacion)==longitud-1:
                    piezas[rotacion]=rotaciones_pieza[0]
                    continue
                piezas[rotacion]=rotaciones_pieza[rotaciones_pieza.index(rotacion)+1]
    return piezas