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

from scipy.spatial.distance import pdist, squareform

def crear_padres():
    """Es función tiene el proposito de crear posbles combinaciones de ciudades basandose en el arreglo de la variable nodos donde se tiene 
    el nombre que  se le dio a cada ciuadad y la distancia entre ellas"""
# Usamos len(nodos) para que k siempre sea igual al tamaño de la población disponible
    distribucion = random.sample(nodos, k=len(nodos)) 
    
    # LEY 1 del TSP: Regresar al inicio
    primero = distribucion[0]
    distribucion.append(primero)
    return distribucion


def torneo(poblacion, distancias, k):
    """
    Selección por torneo.
    poblacion: La lista de rutas actuales.
    distancias: Una lista con la distancia total de cada ruta en la población.
    k: El tamaño del torneo (cuántos compiten).
    """
    # 1. Elegir k índices al azar de la población
    indices_participantes = random.sample(range(len(poblacion)), k)
    
    # 2. Encontrar cuál de esos participantes tiene la menor distancia
    mejor_indice = indices_participantes[0]
    for idx in indices_participantes:
        if distancias[idx] < distancias[mejor_indice]:
            mejor_indice = idx
            
    # 3. Devolver el ganador del torneo
    return poblacion[mejor_indice]

def crossover_ox(padre,madre):
    ''' Esta función se encarga de hacer un crosover entre dos padres en la cual
    se obta por preserva simpre la priemera mitada del padre y completar con lo que sobra de la madre o segundo padre'''
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

def mutacion_inversion(ruta, probabilidad):
    if random.random() < probabilidad:
        n = len(ruta) - 1 # No tocar el último (retorno)
        i, j = sorted(random.sample(range(n), 2))
        # Invertimos el segmento entre i y j
        ruta[i:j] = reversed(ruta[i:j])
        ruta[-1] = ruta[0] # Mantener Ley 1
    return ruta

try:
    # Pedir al usurio que indique con que formato de archivo va a trabajar con el, ya sea matriz normal, puntos gleoglobales, cordenadas o matriz rara. 
    print("Solución de problema del agente viajero con euristicas")
    print("Ponga 1 si es con matriz")
    print("Ponga 2 si es con lantitud y longitud")
    print("Ponga 3 si es con cordenadas x y y en el plano cartesiano")
    print("Ponga 4 si es una mmatriz estraña")
    print()
    caso = int(input("Indique el formato con el que se va a trabajar en este software: "))
    print()
    # Cargar archivo con información de la base datos de la disntacia entre puntos 
    nombre_archivo = input("Ingrese el nombre de archivo las distancias de los puntos analizar: ")
    print()
    base_datos = pd.read_excel(nombre_archivo, index_col= 0)

    if caso == 1:
        
        nodos = list(base_datos.columns)
        base = len(nodos)  # Esto asegura que 'base' sea EXACTAMENTE el número de ciudades
        matriz_distancias_rapida = base_datos.values
        mapa_nodos = {nodo: i for i, nodo in enumerate(nodos)}
        
        
        matriz_distancias_rapida = base_datos.values
        mapa_nodos = {nodo: i for i, nodo in enumerate(nodos)}
        from scipy.spatial import distance_matrix

        def calcular_d(orden):
            """Esta función realiza el calculo de la distancia en cada ruta que se le ingresa 
            la cual el vaijero realiza."""
            distancia_total = 0
            for camino in range(len(orden) - 1):
                idx_primero = mapa_nodos[orden[camino]]
                idx_siguiente = mapa_nodos[orden[camino+1]]
                distancia_total += matriz_distancias_rapida[idx_primero, idx_siguiente]
                
            return distancia_total
              
        def proceso_algoritmo_genetico():
            """Hacer uso del algoritmo genetico de mejora para hayar cual es la ruta más corta 
            para el ajente viajero. Con una población de 100 y 500 generaciones  """
            
            # Paso 1 crear una población de muchas combinaciones para tener un punto de partida
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
            
            # Paso 2 seleccioanr el mejor luego de una evolución de varias iteraciones. Apromadamente 50
            # nuemro de iteracioens 
            n_pruebas =1000
            # Esto se hace para guardar el tiempo y posbles combinacioens en caso 
            # de haber más de una buena combinación que arrogue el valor más pequeño
            posibles_candidatos = []
            menor_peso = float('inf') # Se parte de infinito para luego ir decendiendo. 
            
            valores = []
            for prueba in range(n_pruebas): 
                # 1. Calculamos las distancias de la población actual (Necesario para el torneo)
                distancias_poblacion = [calcular_d(ind) for ind in poblaciones]
                
                # 2. Encontrar el mejor de momento
                menor_peso_gen = min(distancias_poblacion)
                indice_mejor = distancias_poblacion.index(menor_peso_gen)
                mejor_de_momento = poblaciones[indice_mejor]

                # Actualizar el récord global si es necesario
                if menor_peso_gen < menor_peso:
                    menor_peso = menor_peso_gen
                    posibles_candidatos = [mejor_de_momento]
                elif menor_peso_gen == menor_peso:
                    if mejor_de_momento not in posibles_candidatos:
                        posibles_candidatos.append(mejor_de_momento)

                print(f"Generación: {prueba + 1} | Mejor Distancia: {menor_peso} km")
                
                # 3. Crear la nueva población
                nueva_poblacion = []
                nueva_poblacion.append(mejor_de_momento) # Elitismo
                
                while len(nueva_poblacion) < monton:
                    # Llamada correcta a torneo con k=3
                    progenitor1 = torneo(poblaciones, distancias_poblacion, k=5)
                    progenitor2 = torneo(poblaciones, distancias_poblacion, k=5)
                    
                    resultado = crossover_ox(progenitor1, progenitor2)
                    resultado = mutacion_inversion(resultado, 0.2)
                    
                    if resultado not in nueva_poblacion:
                        nueva_poblacion.append(resultado)
                
                # 4. Reemplazar población vieja con la nueva
                poblaciones = nueva_poblacion
                valores.append(menor_peso)
            
            
            x = list(range(1, len(valores) + 1))

            # Mostrar los resultados
            print()
            print(f"El valor menor de distancia obtendio es de {menor_peso} km")
            print()
            print("Y se obtiene con las sigueintes combinaciones:")
            print()
            contador = 1
            for combinacion_miedo in posibles_candidatos:
                arreglo_miedo = " - ".join(map(str, combinacion_miedo))
                print(f" {contador}:  {arreglo_miedo}")
                contador += 1
        
            plt.plot(x, valores)
            plt.xlabel("Generación")
            plt.ylabel(" Distancia entre nodos")
            plt.title("Cambios con las generaciones")
            plt.grid()
            plt.show()

        proceso_algoritmo_genetico()
        
    elif caso == 2:
        base_datos = pd.read_excel(nombre_archivo, index_col= None)

        #print(base_datos)
        nodos = base_datos.iloc[:, 0].tolist()
        base_datos.columns = base_datos.columns.str.strip()
        mapa_nodos = {nodo: i for i, nodo in enumerate(nodos)}
        
        coordenadas = np.radians(base_datos[['Latitud', 'Longitud']].values)
        
        def calcular_d(orden):
            distancia_total = 0
            radio_tierra = 6371.0
            
            # Recorrido entre nodos
            for i in range(len(orden) - 1):
                idx1 = mapa_nodos[orden[i]]
                idx2 = mapa_nodos[orden[i+1]]
                
                lat1, lon1 = coordenadas[idx1]
                lat2, lon2 = coordenadas[idx2]
                
                # Haversine
                dlat, dlon = lat2 - lat1, lon2 - lon1
                a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
                distancia_total += radio_tierra * (2 * np.arctan2(np.sqrt(a), np.sqrt(1-a)))
                
            # CIERRE: Distancia del último al primero
            idx_fin = mapa_nodos[orden[-1]]
            idx_ini = mapa_nodos[orden[0]]
            lat_f, lon_f = coordenadas[idx_fin]
            lat_i, lon_i = coordenadas[idx_ini]
            
            a_c = np.sin((lat_i-lat_f)/2)**2 + np.cos(lat_f)*np.cos(lat_i)*np.sin((lon_i-lon_f)/2)**2
            distancia_total += radio_tierra * (2 * np.arctan2(np.sqrt(a_c), np.sqrt(1-a_c)))
            
            return distancia_total
                
        def proceso_algoritmo_genetico():
            """Hacer uso del algoritmo genetico de mejora para hayar cual es la ruta más corta 
            para el ajente viajero. Con una población de 100 y 500 generaciones  """
            
            # Paso 1 crear una población de muchas combinaciones para tener un punto de partida
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
            
            # Paso 2 seleccioanr el mejor luego de una evolución de varias iteraciones. Apromadamente 50
            # nuemro de iteracioens 
            n_pruebas =500
            # Esto se hace para guardar el tiempo y posbles combinacioens en caso 
            # de haber más de una buena combinación que arrogue el valor más pequeño
            posibles_candidatos = []
            menor_peso = float('inf') # Se parte de infinito para luego ir decendiendo. 
            
            valores = []
            for prueba in range(n_pruebas): 
                # 1. Calculamos las distancias de la población actual (Necesario para el torneo)
                distancias_poblacion = [calcular_d(ind) for ind in poblaciones]
                
                # 2. Encontrar el mejor de momento
                menor_peso_gen = min(distancias_poblacion)
                indice_mejor = distancias_poblacion.index(menor_peso_gen)
                mejor_de_momento = poblaciones[indice_mejor]

                # Actualizar el récord global si es necesario
                if menor_peso_gen < menor_peso:
                    menor_peso = menor_peso_gen
                    posibles_candidatos = [mejor_de_momento]
                elif menor_peso_gen == menor_peso:
                    if mejor_de_momento not in posibles_candidatos:
                        posibles_candidatos.append(mejor_de_momento)

                print(f"Generación: {prueba + 1} | Mejor Distancia: {menor_peso} km")
                
                # 3. Crear la nueva población
                nueva_poblacion = []
                nueva_poblacion.append(mejor_de_momento) # Elitismo
                
                while len(nueva_poblacion) < monton:
                    # Llamada correcta a torneo con k=3
                    progenitor1 = torneo(poblaciones, distancias_poblacion, k=5)
                    progenitor2 = torneo(poblaciones, distancias_poblacion, k=5)
                    
                    resultado = crossover_ox(progenitor1, progenitor2)
                    resultado = mutacion_inversion(resultado, 0.2)
                    
                    if resultado not in nueva_poblacion:
                        nueva_poblacion.append(resultado)
                
                # 4. Reemplazar población vieja con la nueva
                poblaciones = nueva_poblacion
                valores.append(menor_peso)
            
            
            x = list(range(1, len(valores) + 1))

            # Mostrar los resultados
            print()
            print(f"El valor menor de distancia obtendio es de {menor_peso} km")
            print()
            print("\nY se obtiene con las siguientes combinaciones:")
            contador = 1
            for combinacion_miedo in posibles_candidatos:
                arreglo_miedo = " - ".join(map(str, combinacion_miedo))
                print(f" {contador}:  {arreglo_miedo}")
                contador += 1
        
            plt.plot(x, valores)
            plt.xlabel("Generación")
            plt.ylabel(" Distancia entre nodos")
            plt.title("Cambios con las generaciones")
            plt.grid()
            plt.show()

        proceso_algoritmo_genetico()       
     
    elif caso == 3:
        base_datos = pd.read_excel(nombre_archivo, index_col= None)

        print(base_datos)
        nodos = base_datos.iloc[:, 0].tolist()
        base_datos.columns = base_datos.columns.str.strip()
        mapa_nodos = {nodo: i for i, nodo in enumerate(nodos)}
        
        coordenadas = base_datos[['X', 'Y']].values
        matriz_distancias = squareform(pdist(coordenadas , metric='euclidean'))
        
        def calcular_d(orden):
            # 1. Convertimos los nombres de nodos (a1, a2...) a sus índices (0, 1, 2...)
            indices = [mapa_nodos[n] for n in orden]
        
            # 2. Sumamos las distancias entre nodos consecutivos usando la matriz
            # Esto suma: d(0,1) + d(1,2) + ...
            distancia_total = matriz_distancias[indices[:-1], indices[1:]].sum()
            
            # 3. Sumamos el regreso al origen (Ciclo cerrado)
            distancia_total += matriz_distancias[indices[-1], indices[0]]
            
            return distancia_total
        
        def proceso_algoritmo_genetico():
            """Hacer uso del algoritmo genetico de mejora para hayar cual es la ruta más corta 
            para el ajente viajero. Con una población de 100 y 500 generaciones  """
            
            # Paso 1 crear una población de muchas combinaciones para tener un punto de partida
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
            
            # Paso 2 seleccioanr el mejor luego de una evolución de varias iteraciones. Apromadamente 50
            # nuemro de iteracioens 
            n_pruebas =500
            # Esto se hace para guardar el tiempo y posbles combinacioens en caso 
            # de haber más de una buena combinación que arrogue el valor más pequeño
            posibles_candidatos = []
            menor_peso = float('inf') # Se parte de infinito para luego ir decendiendo. 
            
            valores = []
            for prueba in range(n_pruebas): 
                # 1. Calculamos las distancias de la población actual (Necesario para el torneo)
                distancias_poblacion = [calcular_d(ind) for ind in poblaciones]
                
                # 2. Encontrar el mejor de momento
                menor_peso_gen = min(distancias_poblacion)
                indice_mejor = distancias_poblacion.index(menor_peso_gen)
                mejor_de_momento = poblaciones[indice_mejor]

                # Actualizar el récord global si es necesario
                if menor_peso_gen < menor_peso:
                    menor_peso = menor_peso_gen
                    posibles_candidatos = [mejor_de_momento]
                elif menor_peso_gen == menor_peso:
                    if mejor_de_momento not in posibles_candidatos:
                        posibles_candidatos.append(mejor_de_momento)

                print(f"Generación: {prueba + 1} | Mejor Distancia: {menor_peso} km")
                
                # 3. Crear la nueva población
                nueva_poblacion = []
                nueva_poblacion.append(mejor_de_momento) # Elitismo
                
                while len(nueva_poblacion) < monton:
                    # Llamada correcta a torneo con k=3
                    progenitor1 = torneo(poblaciones, distancias_poblacion, k=10)
                    progenitor2 = torneo(poblaciones, distancias_poblacion, k=10)
                    
                    resultado = crossover_ox(progenitor1, progenitor2)
                    resultado = mutacion_inversion(resultado, 0.1)
                    
                    if resultado not in nueva_poblacion:
                        nueva_poblacion.append(resultado)
                
                # 4. Reemplazar población vieja con la nueva
                poblaciones = nueva_poblacion
                valores.append(menor_peso)
            
            
            x = list(range(1, len(valores) + 1))

            # Mostrar los resultados
            print()
            print(f"El valor menor de distancia obtendio es de {menor_peso} km")
            print()
            print("\nY se obtiene con las siguientes combinaciones:")
            contador = 1
            for combinacion_miedo in posibles_candidatos:
                arreglo_miedo = " - ".join(map(str, combinacion_miedo))
                print(f" {contador}:  {arreglo_miedo}")
                contador += 1
        
            plt.plot(x, valores)
            plt.xlabel("Generación")
            plt.ylabel(" Distancia entre nodos")
            plt.title("Cambios con las generaciones")
            plt.grid()
            plt.show()

        proceso_algoritmo_genetico()        
    
    elif caso == 4:
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
                # Si un lemento es texto o lago así se borra.
                continue

        # Hayar la cantidad de ceros de arreglo para hacer filas
        total_filas = solo_distancias.count(0)
        # Crear una matriz de ceros para rellenar cuando se realice la reparación de los datos. Esto para que tenga el espacio adecuado y así sea más fácil ordenar. 
        # cuando se tenga que recosntruir toda la matriz. ya que la diea es usar esa resocntrucción y depsues usarla con el metdo de matriz completa que ya se había implemnetado antes. 
        matriz_cuadrada = np.zeros((total_filas,total_filas)) # esta es cuadrada ya que sino no se puede formar el conjunto de datos con la diognal de ceros. 
        # Crear variables de contador para formar la matriz
        fila_contador = 0
        columna_contador = 0

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
        # Crear la nueva base de datos con los datos pero arregaldos de mejor forma
        base_datos = pd.DataFrame(matriz_cuadrada, index=puntos, columns=puntos)

        nodos = list(base_datos.columns)
        base = len(nodos)  # Esto asegura que 'base' sea EXACTAMENTE el número de ciudades
        matriz_distancias_rapida = base_datos.values
        mapa_nodos = {nodo: i for i, nodo in enumerate(nodos)}
        
        
        matriz_distancias_rapida = base_datos.values
        mapa_nodos = {nodo: i for i, nodo in enumerate(nodos)}
        from scipy.spatial import distance_matrix

        def calcular_d(orden):
            """Esta función realiza el calculo de la distancia en cada ruta que se le ingresa 
            la cual el vaijero realiza."""
            distancia_total = 0
            for camino in range(len(orden) - 1):
                idx_primero = mapa_nodos[orden[camino]]
                idx_siguiente = mapa_nodos[orden[camino+1]]
                distancia_total += matriz_distancias_rapida[idx_primero, idx_siguiente]
                
            return distancia_total
        
        def proceso_algoritmo_genetico():
            """Hacer uso del algoritmo genetico de mejora para hayar cual es la ruta más corta 
            para el ajente viajero. Con una población de 100 y 500 generaciones  """
            
            # Paso 1 crear una población de muchas combinaciones para tener un punto de partida
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
            
            # Paso 2 seleccioanr el mejor luego de una evolución de varias iteraciones. Apromadamente 50
            # nuemro de iteracioens 
            n_pruebas =1000
            # Esto se hace para guardar el tiempo y posbles combinacioens en caso 
            # de haber más de una buena combinación que arrogue el valor más pequeño
            posibles_candidatos = []
            menor_peso = float('inf') # Se parte de infinito para luego ir decendiendo. 
            
            valores = []
            for prueba in range(n_pruebas): 
                # 1. Calculamos las distancias de la población actual (Necesario para el torneo)
                distancias_poblacion = [calcular_d(ind) for ind in poblaciones]
                
                # 2. Encontrar el mejor de momento
                menor_peso_gen = min(distancias_poblacion)
                indice_mejor = distancias_poblacion.index(menor_peso_gen)
                mejor_de_momento = poblaciones[indice_mejor]

                # Actualizar el récord global si es necesario
                if menor_peso_gen < menor_peso:
                    menor_peso = menor_peso_gen
                    posibles_candidatos = [mejor_de_momento]
                elif menor_peso_gen == menor_peso:
                    if mejor_de_momento not in posibles_candidatos:
                        posibles_candidatos.append(mejor_de_momento)

                print(f"Generación: {prueba + 1} | Mejor Distancia: {menor_peso} km")
                
                # 3. Crear la nueva población
                nueva_poblacion = []
                nueva_poblacion.append(mejor_de_momento) # Elitismo
                
                while len(nueva_poblacion) < monton:
                    # Llamada correcta a torneo con k=3
                    progenitor1 = torneo(poblaciones, distancias_poblacion, k=5)
                    progenitor2 = torneo(poblaciones, distancias_poblacion, k=5)
                    
                    resultado = crossover_ox(progenitor1, progenitor2)
                    resultado = mutacion_inversion(resultado, 0.2)
                    
                    if resultado not in nueva_poblacion:
                        nueva_poblacion.append(resultado)
                
                # 4. Reemplazar población vieja con la nueva
                poblaciones = nueva_poblacion
                valores.append(menor_peso)
            
            
            x = list(range(1, len(valores) + 1))

            # Mostrar los resultados
            print()
            print(f"El valor menor de distancia obtendio es de {menor_peso} km")
            print()
            print("Y se obtiene con las sigueintes combinaciones:")
            print()
            contador = 1
            for combinacion_miedo in posibles_candidatos:
                arreglo_miedo = " - ".join(map(str, combinacion_miedo))
                print(f" {contador}:  {arreglo_miedo}")
                contador += 1
        
            plt.plot(x, valores)
            plt.xlabel("Generación")
            plt.ylabel(" Distancia entre nodos")
            plt.title("Cambios con las generaciones")
            plt.grid()
            plt.show()

        proceso_algoritmo_genetico()
  
    else: 
        print("Usuario lea bien")

except:
      # En caso de algun problema notificar al usario de forma amable. 
    print()
    print("Se equivoco en el nombre del archivo, no esta en misma carpeta o ese no tiene el formato que corresponde al numero que puso.")
    print("Tambien es posble que no pusiera lago que es un número del 1 al 4 cuando se le pido hacer eso. ")
    print("Ponga bien la extensión .xlsx y el número porque el problema es de capa 8 y no esta en el software sino entre el escritorio y la silla.") 
    print()

