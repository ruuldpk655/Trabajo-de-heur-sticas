'''
        Universidad de Costa Rica
            Sede Occidente  

        Escuela de Ingeniería Industrial  

    Modelos Estocásticos y Heurísticos para la Industria

    Caso: Problema del agente viajero
        
            Estudiantes:
        Melany Vargas Blanco C28100 
        Britny Mendoza Murillo C14736
        Raúl Evelio Fernndez Vargas C02975  
        Joseph Alpizar Alpizar C00240

        Profesor: Ronny Pacheco Segura 
 
                    I-2026
'''

# Inicio del código
# Importar libreria de Pandas
import pandas as pd
# Importar libreria matplotlib
import matplotlib.pyplot as plt
# Importar libre ramdfom 
import random
# Importar numpy
import numpy as np
# Importar pdist, squareform
from scipy.spatial.distance import pdist, squareform

'''Para este código se tiene que se esocgio priemro poner las funciones que se encargan de hacer el algorimot genetico como crear padres, la mutación 
el toerneo (el cual se esciogio por prsnetar resultados más veloces en comparación con la ruleta almneos para este código) y  el crossover'''

# Crear función crear_padres
def crear_padres():
    """Es función tiene el proposito de crear posbles combinaciones de ciudades basandose en el arreglo de la variable nodos donde se tiene 
    el nombre que  se le dio a cada ciuadad y la distancia entre ellas"""
    # Se crea una lista con las ciudades nombres de los puntos de referencia para indicar ciudades o algo similar
    distribucion = random.sample(nodos, k=len(nodos)) 
    # Se pone el priemer elemnto de la ruta al finalk para cerrar el bucle. 
    primero = distribucion[0]
    distribucion.append(primero)
    return distribucion

# Crear función torneo
def torneo(poblacion, distancias, k):
    """Esta función se encarga de hacer la selección de los elekntos d ela poblasción y poner los a compertir para decir el mejor """
    # Elegir a los peleaodres dle  Tenkaichi Budōkai
    peleadores = random.sample(range(len(poblacion)), k)
    # Encontrra cual es Goku en esos participantes
    # Ver el indice del priemer elemento de los peleadores
    ganador = peleadores[0]
    # Recorrer todos los peledores hasta hayar el que tiene mayor nivel de poder
    for participante in peleadores:
        if distancias[participante] < distancias[ganador]:
            ganador = participante
            
    # 3. Devolver el Goku del torneo
    return poblacion[ganador]

# Crear función de crossover_ox
def crossover_ox(padre,madre):
    ''' Esta función se encarga de hacer un crosover entre dos padres en la cual
    se obta por preservar simpre la priemera mitada del padre y completar con lo que sobra de la madre o segundo padre'''
    # Obtner la mitad
    extension = len(padre)
    mitad = int(extension/2) 
    
    # Crear hijo  a traves de la lista
    hijo = []
    # Cojn esto se preserva simpre la primera mitadad del padre
    for i in range(0, mitad):
        hijo.append(padre[i])
        
    # Elementos sobrantes de la madre
    sobrantes = []
    for elemento in madre:
        if elemento not in hijo:
            sobrantes.append(elemento)
            
    # Completar el hijo con lo que hace falta
    hijo.extend(sobrantes)
    # Poner punto de retorno de forma que regrese desde donde vino. 
    hijo.append(hijo[0])
    # Delvolver el hijo
    return hijo

# Crear función de mutacion_inversion. Se probo una mutación distinta a la de swap porque ¿porque no?
def mutacion_inversion(ruta, radiacion):
    if random.random() < radiacion:
        # Dejar sin cambios en el ultimo elemnto de la ruta
        ultmimo = len(ruta) - 1 
        # Entre que valores se hara el cambio dejando el priemr y ultmo lemento de la lsita intactos
        i, j = sorted(random.sample(range(1, ultmimo), 2))
        # Realizar la inversión
        ruta[i:j] = reversed(ruta[i:j])
    # Delvover la ruta con la inversión
    return ruta



# A partir de este punto empieza a ingresar los dtos desde disfenrtes formatos para probar el porblema del agente viajero. 
try:
    # Pedir al usurio que indique con que formato de archivo va a trabajar con el, ya sea matriz normal, puntos gleoglobales, cordenadas o matriz rara. 
    print("Solución de problema del agente viajero con euristicas")
    print("Ponga 1 si es con matriz")
    print("Ponga 2 si es con lantitud y longitud")
    print("Ponga 3 si es con cordenadas x y y en el plano cartesiano")
    print("Ponga 4 si es una matriz estraña")
    print()
    caso = int(input("Indique el formato con el que se va a trabajar en este software: "))
    print()
    # Cargar archivo con información de la base datos de la disntacia entre puntos 
    nombre_archivo = input("Ingrese el nombre de archivo las distancias de los puntos analizar: ")
    print()
    base_datos = pd.read_excel(nombre_archivo, index_col= 0)
    
    # Si se tiene el caso 1 quiere decir que escogio matriz
    if caso == 1:
        # Hacer un mapa de los nodos que se van a suar para identificar las ciudades. 
        nodos = list(base_datos.columns)
        base = len(nodos) 
        matriz_distancias_rapida = base_datos.values
        mapa_nodos = {nodo: i for i, nodo in enumerate(nodos)}
        
        # Crear una matriz con los datos de la base de datos para hacer los calculos de distancias
        matriz_distancias_rapida = base_datos.values
        mapa_nodos = {nodo: i for i, nodo in enumerate(nodos)}
        
        # Crear matriz de calculo de distancias
        def calcular_d(orden):
            """Esta función realiza el calculo de la distancia en cada ruta que se le ingresa la cual el vaijero podría realiza."""
            # Se define una distancia inicial igual a cero para sumalre datos
            distancia_total = 0
            for camino in range(len(orden) - 1):
                # Obtener ubicaciones de los puntos que se tienen en la ruta a analizar
                punto_1 = mapa_nodos[orden[camino]]
                punto_2 = mapa_nodos[orden[camino+1]]
                # Obtenr la distancia de la matriz de distancias rapidas y sumarlo al valor total de distancias
                distancia_total += matriz_distancias_rapida[punto_1, punto_2]
            # Devolver el valor de distancia total
            return distancia_total
              
        def proceso_algoritmo_genetico():
            """Hacer uso del algoritmo genetico de mejora para hayar cual es la ruta más corta 
            para el ajente viajero. Con una población de 100 y 1000 generaciones, pero eso puede 
            variar segun la necesidad del usuario"""
            
            # Crear una población de muchas combinaciones para tener un punto de partida
            # Crear lista vacia con las muchas pisbles nuevas poblaciones
            poblaciones = []
            # Dar numero de individuos para hacer más general el código
            monton = 100
            contador= 0
            while contador <= monton:
                # Empezar a crear cada meimbro con la función de creaar padres, todos distintos
                people = crear_padres()
                if people not in poblaciones:
                    poblaciones.append(people)
                    contador = contador +1
            
            # Paso 2 seleccioanr el mejor luego de una evolución de varias iteraciones. Apromadamente 1000
            # Numero de generaciones 
            n_pruebas =1000
            # Esto se hace para almcenear cual es la mejor dintacia y su respectiva ruta
            posibles_candidatos = []
            # Se llama menor peso, porque viene del porceso asginación que funciona simialr y  dio pereza cambiarlo porque ya funciona. 
            # Y lo que funciona no se toca
            menor_peso = float('inf') # Se parte de infinito para luego ir decendiendo. 
            # Crear lista vacía para despues tener valores para el grafico. 
            valores = []
            for prueba in range(n_pruebas): 
                # Calcular distancias de la población actual entre puntos de la población actual
                distancias_poblacion = [calcular_d(camino) for camino in poblaciones]
                
                #  Encontrar el mejor de momento
                menor_peso_gen = min(distancias_poblacion)
                indice_mejor = distancias_poblacion.index(menor_peso_gen)
                mejor_de_momento = poblaciones[indice_mejor]

                # Actualizar el valor de la distancia si es necesario
                if menor_peso_gen < menor_peso:
                    menor_peso = menor_peso_gen
                    posibles_candidatos = [mejor_de_momento]
                elif menor_peso_gen == menor_peso:
                    if mejor_de_momento not in posibles_candidatos:
                        posibles_candidatos.append(mejor_de_momento)

                # Mostrar al usario por donde se va para que sepa que esta pasando
                print(f"Generación: {prueba + 1}. Mejor distancia de momento: {menor_peso} km")
                
                # Crear la nueva población hatsa que sea igual a la cantidad de la población original
                nueva_poblacion = []
                nueva_poblacion.append(mejor_de_momento) 
                
                while len(nueva_poblacion) < monton:
                    # Obtener padres con torneo, con 5 particpantes 
                    progenitor1 = torneo(poblaciones, distancias_poblacion, k=5)
                    progenitor2 = torneo(poblaciones, distancias_poblacion, k=5)
                    # Realizar mutación y crossover
                    resultado = crossover_ox(progenitor1, progenitor2)
                    resultado = mutacion_inversion(resultado, 0.2)
                    # Añádir el nuevo iembro si no etaba antes en la población. 
                    if resultado not in nueva_poblacion:
                        nueva_poblacion.append(resultado)
                
                # Reemplazar población vieja con la nueva
                poblaciones = nueva_poblacion
                valores.append(menor_peso)
            
            # Crear un intervalo de variable indepenidente para graficar
            x = list(range(1, len(valores) + 1))

            # Mostrar los resultados
            print()
            print(f"El valor menor de distancia obtendio es de {menor_peso} km")
            print()
            print("Y se obtiene con las siguiente combinación:")
            print()
            contador = 1
            # Mostrar combinación
            for combinacion_miedo in posibles_candidatos:
                arreglo_miedo = " - ".join(map(str, combinacion_miedo))
                print(f" {contador}:  {arreglo_miedo}")
                contador += 1

            # Mostrar grafico
            plt.plot(x, valores, color="red") # El grafico se escogio de color rojo
            plt.xlabel("Generación")
            plt.ylabel("Distancia entre nodos 1/km")
            plt.title("Cambios con las generaciones")
            plt.grid()
            plt.show()

        # Llamar a la función que realiza el proceso 
        proceso_algoritmo_genetico()
    
    # Si se tiene el caso 2 quiere decir que escogio cordenadas geograficas
    elif caso == 2:
        # Se carga la base de dtaos nuevamente pero tomando en cuenta la priemra columna de nodos con los puntos geoglobales.
        base_datos = pd.read_excel(nombre_archivo, index_col= None)

        # Se crea la matriz de nodos
        nodos = base_datos.iloc[:, 0].tolist()
        base_datos.columns = base_datos.columns.str.strip()
        mapa_nodos = {nodo: i for i, nodo in enumerate(nodos)}
        
        # Se crea una matriz de nodos con los puntos globales
        coordenadas = np.radians(base_datos[['Latitud', 'Longitud']].values)
        
        def calcular_d(orden):
            """Esta función realiza el calculo de la distancia en cada ruta que se le ingresa la cual el vaijero podría realiza.
            Pero usando las cordenadas de tierra"""
            # variable para sumar la distancia total recorrida
            distancia_total = 0
            # Radio de la tierra
            radio_tierra = 6371.0
            
            # Realizar el recorrido entre nodos o puntos dada por la ruta en el termino orden. 
            for i in range(len(orden) - 1):
                posición_1 = mapa_nodos[orden[i]]
                posición_2 = mapa_nodos[orden[i+1]]
                
                latitud1, longitud1 = coordenadas[posición_1]
                latitud2, longitud2 = coordenadas[posición_2]
                
                # Obter dintacia mediate  metodo de Haversine
                dlat, dlon = latitud2 - latitud1, longitud2 - longitud1
                a = np.sin(dlat/2)**2 + np.cos(latitud1)*np.cos(latitud2)*np.sin(dlon/2)**2
                distancia_total += radio_tierra * (2 * np.arctan2(np.sqrt(a), np.sqrt(1-a)))
                
            # Hacer el priemer punto el ultimo
            posicion_final= mapa_nodos[orden[-1]]
            posicion_inicial = mapa_nodos[orden[0]]
            lat_f, lon_f = coordenadas[posicion_final]
            lat_i, lon_i = coordenadas[posicion_inicial]
            
            a_c = np.sin((lat_i-lat_f)/2)**2 + np.cos(lat_f)*np.cos(lat_i)*np.sin((lon_i-lon_f)/2)**2
            distancia_total += radio_tierra * (2 * np.arctan2(np.sqrt(a_c), np.sqrt(1-a_c)))
            # Devolver la suma total
            return distancia_total
                
        def proceso_algoritmo_genetico():
                """Hacer uso del algoritmo genetico de mejora para hayar cual es la ruta más corta 
            para el ajente viajero. Con una población de 100 y 1000 generaciones, pero eso puede 
            variar segun la necesidad del usuario"""
            
                # Crear una población de muchas combinaciones para tener un punto de partida
                # Crear lista vacia con las muchas pisbles nuevas poblaciones
                poblaciones = []
                # Dar numero de individuos para hacer más general el código
                monton = 100
                contador= 0
                while contador <= monton:
                    # Empezar a crear cada meimbro con la función de creaar padres, todos distintos
                    people = crear_padres()
                    if people not in poblaciones:
                        poblaciones.append(people)
                        contador = contador +1
                
                # Paso 2 seleccioanr el mejor luego de una evolución de varias iteraciones. Apromadamente 1000
                # Numero de generaciones 
                n_pruebas =1000
                # Esto se hace para almcenear cual es la mejor dintacia y su respectiva ruta
                posibles_candidatos = []
                # Se llama menor peso, porque viene del porceso asginación que funciona simialr y  dio pereza cambiarlo porque ya funciona. 
                # Y lo que funciona no se toca
                menor_peso = float('inf') # Se parte de infinito para luego ir decendiendo. 
                # Crear lista vacía para despues tener valores para el grafico. 
                valores = []
                for prueba in range(n_pruebas): 
                    # Calcular distancias de la población actual entre puntos de la población actual
                    distancias_poblacion = [calcular_d(camino) for camino in poblaciones]
                    
                    #  Encontrar el mejor de momento
                    menor_peso_gen = min(distancias_poblacion)
                    indice_mejor = distancias_poblacion.index(menor_peso_gen)
                    mejor_de_momento = poblaciones[indice_mejor]

                    # Actualizar el valor de la distancia si es necesario
                    if menor_peso_gen < menor_peso:
                        menor_peso = menor_peso_gen
                        posibles_candidatos = [mejor_de_momento]
                    elif menor_peso_gen == menor_peso:
                        if mejor_de_momento not in posibles_candidatos:
                            posibles_candidatos.append(mejor_de_momento)

                    # Mostrar al usario por donde se va para que sepa que esta pasando
                    print(f"Generación: {prueba + 1}. Mejor distancia de momento: {menor_peso} km")
                    
                    # Crear la nueva población hatsa que sea igual a la cantidad de la población original
                    nueva_poblacion = []
                    nueva_poblacion.append(mejor_de_momento) 
                    
                    while len(nueva_poblacion) < monton:
                        # Obtener padres con torneo, con 5 particpantes 
                        progenitor1 = torneo(poblaciones, distancias_poblacion, k=5)
                        progenitor2 = torneo(poblaciones, distancias_poblacion, k=5)
                        # Realizar mutación y crossover
                        resultado = crossover_ox(progenitor1, progenitor2)
                        resultado = mutacion_inversion(resultado, 0.2)
                        # Añádir el nuevo iembro si no etaba antes en la población. 
                        if resultado not in nueva_poblacion:
                            nueva_poblacion.append(resultado)
                    
                    # Reemplazar población vieja con la nueva
                    poblaciones = nueva_poblacion
                    valores.append(menor_peso)
                
                # Crear un intervalo de variable indepenidente para graficar
                x = list(range(1, len(valores) + 1))

                # Mostrar los resultados
                print()
                print(f"El valor menor de distancia obtendio es de {menor_peso} km")
                print()
                print("Y se obtiene con las siguiente combinación:")
                print()
                contador = 1
                # Mostrar combinación
                for combinacion_miedo in posibles_candidatos:
                    arreglo_miedo = " - ".join(map(str, combinacion_miedo))
                    print(f" {contador}:  {arreglo_miedo}")
                    contador += 1

                # Mostrar grafico
                plt.plot(x, valores, color="green") # El grafico se escogio de color verde
                plt.xlabel("Generación")
                plt.ylabel("Distancia entre nodos 1/km")
                plt.title("Cambios con las generaciones")
                plt.grid()
                plt.show()

        # Llamar a la función que realiza el proceso 
        proceso_algoritmo_genetico()
           
    # Si se tiene el caso 3 quiere decir que escogio cordenadas X y Y
    elif caso == 3:
        # Se vulve anombra la base de datos para que tome en cuenta la columna de nodos
        base_datos = pd.read_excel(nombre_archivo, index_col= None)

        # Realizar el arreglo con los nodos
        nodos = base_datos.iloc[:, 0].tolist()
        base_datos.columns = base_datos.columns.str.strip()
        mapa_nodos = {nodo: i for i, nodo in enumerate(nodos)}
        
        # Crear matriz con coodenadas X y Y
        coordenadas = base_datos[['X', 'Y']].values
        # Matriz con las ditancias entre puntos
        matriz_distancias = squareform(pdist(coordenadas , metric='euclidean'))
        
        def calcular_d(orden):
            """Esta matriz realiza el caluclo de la distancia entre cordanadas dadas """
            # Obtner posición de cada nodo
            indices = [mapa_nodos[n] for n in orden]
        
            # SUmar las dintacias entre los puntos datos por la ruta en el arguekmnto orden
            distancia_total = matriz_distancias[indices[:-1], indices[1:]].sum()
            
            # Sumar el regreso al origen
            distancia_total += matriz_distancias[indices[-1], indices[0]]
            # Devolver la distancia total calculada
            return distancia_total
        
        def proceso_algoritmo_genetico():
                """Hacer uso del algoritmo genetico de mejora para hayar cual es la ruta más corta 
            para el ajente viajero. Con una población de 100 y 1000 generaciones, pero eso puede 
            variar segun la necesidad del usuario"""
            
                # Crear una población de muchas combinaciones para tener un punto de partida
                # Crear lista vacia con las muchas pisbles nuevas poblaciones
                poblaciones = []
                # Dar numero de individuos para hacer más general el código
                monton = 100
                contador= 0
                while contador <= monton:
                    # Empezar a crear cada meimbro con la función de creaar padres, todos distintos
                    people = crear_padres()
                    if people not in poblaciones:
                        poblaciones.append(people)
                        contador = contador +1
                
                # Paso 2 seleccioanr el mejor luego de una evolución de varias iteraciones. Apromadamente 1000
                # Numero de generaciones 
                n_pruebas =1000
                # Esto se hace para almcenear cual es la mejor dintacia y su respectiva ruta
                posibles_candidatos = []
                # Se llama menor peso, porque viene del porceso asginación que funciona simialr y  dio pereza cambiarlo porque ya funciona. 
                # Y lo que funciona no se toca
                menor_peso = float('inf') # Se parte de infinito para luego ir decendiendo. 
                # Crear lista vacía para despues tener valores para el grafico. 
                valores = []
                for prueba in range(n_pruebas): 
                    # Calcular distancias de la población actual entre puntos de la población actual
                    distancias_poblacion = [calcular_d(camino) for camino in poblaciones]
                    
                    #  Encontrar el mejor de momento
                    menor_peso_gen = min(distancias_poblacion)
                    indice_mejor = distancias_poblacion.index(menor_peso_gen)
                    mejor_de_momento = poblaciones[indice_mejor]

                    # Actualizar el valor de la distancia si es necesario
                    if menor_peso_gen < menor_peso:
                        menor_peso = menor_peso_gen
                        posibles_candidatos = [mejor_de_momento]
                    elif menor_peso_gen == menor_peso:
                        if mejor_de_momento not in posibles_candidatos:
                            posibles_candidatos.append(mejor_de_momento)

                    # Mostrar al usario por donde se va para que sepa que esta pasando
                    print(f"Generación: {prueba + 1}. Mejor distancia de momento: {menor_peso} km")
                    
                    # Crear la nueva población hatsa que sea igual a la cantidad de la población original
                    nueva_poblacion = []
                    nueva_poblacion.append(mejor_de_momento) 
                    
                    while len(nueva_poblacion) < monton:
                        # Obtener padres con torneo, con 5 particpantes 
                        progenitor1 = torneo(poblaciones, distancias_poblacion, k=5)
                        progenitor2 = torneo(poblaciones, distancias_poblacion, k=5)
                        # Realizar mutación y crossover
                        resultado = crossover_ox(progenitor1, progenitor2)
                        resultado = mutacion_inversion(resultado, 0.2)
                        # Añádir el nuevo iembro si no etaba antes en la población. 
                        if resultado not in nueva_poblacion:
                            nueva_poblacion.append(resultado)
                    
                    # Reemplazar población vieja con la nueva
                    poblaciones = nueva_poblacion
                    valores.append(menor_peso)
                
                # Crear un intervalo de variable indepenidente para graficar
                x = list(range(1, len(valores) + 1))

                # Mostrar los resultados
                print()
                print(f"El valor menor de distancia obtendio es de {menor_peso} km")
                print()
                print("Y se obtiene con las siguiente combinación:")
                print()
                contador = 1
                # Mostrar combinación
                for combinacion_miedo in posibles_candidatos:
                    arreglo_miedo = " - ".join(map(str, combinacion_miedo))
                    print(f" {contador}:  {arreglo_miedo}")
                    contador += 1

                # Mostrar grafico
                plt.plot(x, valores) 
                plt.xlabel("Generación")
                plt.ylabel("Distancia entre nodos 1/km")
                plt.title("Cambios con las generaciones")
                plt.grid()
                plt.show()

        # Llamar a la función que realiza el proceso 
        proceso_algoritmo_genetico()       
    
    # Si se tiene el caso 4 quiere decir que escogio la matriz rara
    elif caso == 4:
        # Se crea una base de datos con los datos ordenados de forma extraña
        base_compleja= pd.read_excel(nombre_archivo, header=None)
        # Crear una lista con todos los elementos del arreglo donde solo se tiene la parte inferior de una matriz ordenada por líneas
        todo_junto = base_compleja.stack().tolist()

        # Quitar cosas que no vienen al caso para acomodar los datos en una matriz. 
        solo_distancias = []
        for elemento in todo_junto:
            try:
               numeros = float(elemento)
                # Se evalua que los elemenstos no sean un conjunto vacio
               if not np.isnan(numeros):
                    solo_distancias.append(numeros)
            except ValueError:
                # Si un elmento es texto o algo así se borra.
                continue

        # Hayar la cantidad de ceros de arreglo para hacer filas
        total_filas = solo_distancias.count(0)
        # Crear una matriz de ceros para rellenar cuando se realice la reparación de los datos. Esto para que tenga el espacio adecuado y así sea más fácil ordenar. 
        # cuando se tenga que recosntruir toda la matriz. ya que la diea es usar esa resocntrucción y depsues usarla con el metdo de matriz completa que ya se había implemnetado antes. 
        matriz_cuadrada = np.zeros((total_filas,total_filas)) # esta es cuadrada ya que sino no se puede formar el conjunto de datos con la diognal de ceros. 
        # Crear variables de contador para formar la matriz
        fila_contador = 0
        columna_contador = 0
        # Formar la matriz cuadrada con diagonal de ceros
        for valor in solo_distancias:
            if fila_contador < total_filas:
                # Ubicar en la matriz cuadrada las posciones tanto un lado como la otro de la diagonal. 
                matriz_cuadrada[fila_contador, columna_contador] = valor
                matriz_cuadrada[columna_contador, fila_contador] = valor
                # Evaluar cuando se llega a un cero para hacer el cambio de fila
                if valor == 0: 
                    fila_contador += 1 # Si se llega a cero se cambia a una nueva fila, pero se reinicia la columna 
                    columna_contador = 0
                else:
                    # Si aun no se cambia de fila se cambia de columna
                    columna_contador += 1

        # Darle encabezados a al arreglo basador en la letra a como a1, a2, a3, ... esto puee variar segun se requiera. 
        puntos = [f'a{i+1}' for i in range(total_filas)]
        # Crear la nueva base de datos con los datos pero arregaldos de mejor forma matriz como en el caso 1
        base_datos = pd.DataFrame(matriz_cuadrada, index=puntos, columns=puntos)
        
        # Crar arreglo de nodos
        nodos = list(base_datos.columns)
        base = len(nodos)  # Esto asegura que 'base' sea EXACTAMENTE el número de ciudades
        matriz_distancias_rapida = base_datos.values
        mapa_nodos = {nodo: i for i, nodo in enumerate(nodos)}
        # Pasar a matriz la base de datos para el calculo de distancias
        matriz_distancias_rapida = base_datos.values
        mapa_nodos = {nodo: i for i, nodo in enumerate(nodos)}
        
        
        def calcular_d(orden):
            """Esta función realiza el calculo de la distancia en cada ruta que se le ingresa la cual el vaijero podría realiza.
            Es la misma que para el caso 1"""
            # Se define una distancia inicial igual a cero para sumalre datos
            distancia_total = 0
            for camino in range(len(orden) - 1):
                # Obtener ubicaciones de los puntos que se tienen en la ruta a analizar
                punto_1 = mapa_nodos[orden[camino]]
                punto_2 = mapa_nodos[orden[camino+1]]
                # Obtenr la distancia de la matriz de distancias rapidas y sumarlo al valor total de distancias
                distancia_total += matriz_distancias_rapida[punto_1, punto_2]
            # Devolver el valor de distancia total
            return distancia_total
        
        def proceso_algoritmo_genetico():
                """Hacer uso del algoritmo genetico de mejora para hayar cual es la ruta más corta 
            para el ajente viajero. Con una población de 100 y 1000 generaciones, pero eso puede 
            variar segun la necesidad del usuario"""
            
                # Crear una población de muchas combinaciones para tener un punto de partida
                # Crear lista vacia con las muchas pisbles nuevas poblaciones
                poblaciones = []
                # Dar numero de individuos para hacer más general el código
                monton = 100
                contador= 0
                while contador <= monton:
                    # Empezar a crear cada meimbro con la función de creaar padres, todos distintos
                    people = crear_padres()
                    if people not in poblaciones:
                        poblaciones.append(people)
                        contador = contador +1
                
                # Paso 2 seleccioanr el mejor luego de una evolución de varias iteraciones. Apromadamente 1000
                # Numero de generaciones 
                n_pruebas =1000
                # Esto se hace para almcenear cual es la mejor dintacia y su respectiva ruta
                posibles_candidatos = []
                # Se llama menor peso, porque viene del porceso asginación que funciona simialr y  dio pereza cambiarlo porque ya funciona. 
                # Y lo que funciona no se toca
                menor_peso = float('inf') # Se parte de infinito para luego ir decendiendo. 
                # Crear lista vacía para despues tener valores para el grafico. 
                valores = []
                for prueba in range(n_pruebas): 
                    # Calcular distancias de la población actual entre puntos de la población actual
                    distancias_poblacion = [calcular_d(camino) for camino in poblaciones]
                    
                    #  Encontrar el mejor de momento
                    menor_peso_gen = min(distancias_poblacion)
                    indice_mejor = distancias_poblacion.index(menor_peso_gen)
                    mejor_de_momento = poblaciones[indice_mejor]

                    # Actualizar el valor de la distancia si es necesario
                    if menor_peso_gen < menor_peso:
                        menor_peso = menor_peso_gen
                        posibles_candidatos = [mejor_de_momento]
                    elif menor_peso_gen == menor_peso:
                        if mejor_de_momento not in posibles_candidatos:
                            posibles_candidatos.append(mejor_de_momento)

                    # Mostrar al usario por donde se va para que sepa que esta pasando
                    print(f"Generación: {prueba + 1}. Mejor distancia de momento: {menor_peso} km")
                    
                    # Crear la nueva población hatsa que sea igual a la cantidad de la población original
                    nueva_poblacion = []
                    nueva_poblacion.append(mejor_de_momento) 
                    
                    while len(nueva_poblacion) < monton:
                        # Obtener padres con torneo, con 5 particpantes 
                        progenitor1 = torneo(poblaciones, distancias_poblacion, k=5)
                        progenitor2 = torneo(poblaciones, distancias_poblacion, k=5)
                        # Realizar mutación y crossover
                        resultado = crossover_ox(progenitor1, progenitor2)
                        resultado = mutacion_inversion(resultado, 0.2)
                        # Añádir el nuevo iembro si no etaba antes en la población. 
                        if resultado not in nueva_poblacion:
                            nueva_poblacion.append(resultado)
                    
                    # Reemplazar población vieja con la nueva
                    poblaciones = nueva_poblacion
                    valores.append(menor_peso)
                
                # Crear un intervalo de variable indepenidente para graficar
                x = list(range(1, len(valores) + 1))

                # Mostrar los resultados
                print()
                print(f"El valor menor de distancia obtendio es de {menor_peso} km")
                print()
                print("Y se obtiene con las siguiente combinación:")
                print()
                contador = 1
                # Mostrar combinación
                for combinacion_miedo in posibles_candidatos:
                    arreglo_miedo = " - ".join(map(str, combinacion_miedo))
                    print(f" {contador}:  {arreglo_miedo}")
                    contador += 1

                # Mostrar grafico
                plt.plot(x, valores, color="orange") # Se pone en color naranja 
                plt.xlabel("Generación")
                plt.ylabel("Distancia entre nodos 1/km")
                plt.title("Cambios con las generaciones")
                plt.grid()
                plt.show()

        # Llamar a la función que realiza el proceso 
        proceso_algoritmo_genetico()       
  
    else: 
        print("Usuario lea bien por favor")

except:
      # En caso de algun problema notificar al usario de forma amable. 
    print()
    print("Se equivoco en el nombre del archivo, no esta en misma carpeta o ese no tiene el formato que corresponde al numero que puso.")
    print()
    print("Tambien es posible que no pusiera algo que es un número del 1 al 4 cuando fue lo unico que se le pidio hacer eso. ")
    print()
    print("Ponga bien la extensión .xlsx y el número, porque el problema es de capa 8 y no esta en el software sino entre el escritorio y la silla.".upper()) 
    print()
    print("Por ello Usuario lea bien por favor".upper())
    print()

