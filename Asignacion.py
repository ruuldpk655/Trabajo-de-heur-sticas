'''
        Universidad de Costa Rica
            Sede Occidente  

        Escuela de Ingeniería Industrial  

    Modelos Estocásticos y Heurísticos para la Industria

    Caso: Diseño de una heurística para asignación de empleados 
        
            Estudiantes:
        Melany Vargas Blanco C28100 
        Britny Mendoza Murillo C14736
        Raúl Evelio Fernndez Vargas C02975  
        Joseph Alpizar Alpizar C00240 

        Profesor: Ronny Pacheco Segura 
 
                    I-2026
'''


'''Nota importante, todo lo que parece código pero esta como comentario son pruebas que se hicierón, estan de esa forma por aquello que se deba hacer pruebas
en caso de querer cambiar el codigo o ver cosas con el'''
# Muchos comentarios son como son para alegrar el momento mientras se hace el código. No tomar personal. 

# Inicio del código
# Importar libreria de Pandas
import pandas as pd
# Importar libreria matplotlib
import matplotlib.pyplot as plt
# Importar libre ramdfom 
import random


try:
    # Cargar archivo con información de la base datos de la empresa que tiene  los desplazamientos 
    # entre nodos y el tiempo de elaboración en cada uno de ellos
    nombre_archivo = input("Ingrese el nombre de archivo con los trabajadores: ")
    base_datos = pd.read_excel(nombre_archivo)

    # Obtener el número de trabajadores, esta sera una variabnle global
    base = base_datos.index.size
    # Tener lista de trabajadores
    trabajadores = base_datos.iloc[:, 0].to_list()

    posible = [3,5,7,1,6,4,2,8]
    posible_2= [8,2,4,6,1,7,5,3]

    # Crear Función para calcualr el peso por la tardanza
    def calcular_wi(orden): # (1,2, 3, 4 5, 6, 7, 8 )
        '''Crear  función para calular wi.Ti'''
        # Matriz del nuevo orden
        matriz = []
        for i in range(len(orden)):
            elementos = base_datos.iloc[orden[i] -1 ].to_list()
            matriz.append(elementos)
        # Calcualar Ci
        # Tiempo acumulado
        tiempo_acumulado = 0
        for fila in matriz:
            fila[2] = tiempo_acumulado + fila[1]
            tiempo_acumulado =  fila[2]
        # Calcualar Ti
        for fila in matriz:
            tiempo_ti= fila[2] - fila[3]
            #print(tiempo_ti)
            if  tiempo_ti < 0: 
                fila[5] = 0
            else:
                fila[5] = tiempo_ti
        # Calcualar TiWi
        suma_tiempo = 0
        for fila in matriz:
            fila[6] = fila[5]*fila[4]
            suma_tiempo = suma_tiempo + fila[6]
        return suma_tiempo
    
    # Crear función para generar el número de padres 
    def crear_padres():
        """Es función tiene el proposito de crear posibles combinaciones laeatorias de trabajadores que van desd el 1 hasta 
        el número total a asignar que se reuqiera de estos"""
        distribucion= random.sample(trabajadores, k = base)
        # Devolver distribución
        return distribucion

    def comparar_padres_identicos(padre, madre):
        '''Esta función se encagra de ver que si dos padres son igales entre sí'''
        # Evaluar condición de iguladad:
        condicion = 0
        for i in range(0,len(padre)):
            if padre[i] == madre[i]:
                condicion += 1
        if condicion == len(padre): # Si son igaules se devulve que los son y si no, pues no.
            return "iguales"
        else:
            return "diferentes"
            
    def ruleta(poblacion, pesos):
        '''Esta función se encgra de relaizar el algorimo de la ruleta '''
        # Generar un número aleatorio entre 0 y la suma total de los pesos pre-calculados
        # Obtner el total
        suma_total = sum(pesos)
        # Realializar el sorteo, donde sale el que le toca exponer primero.  
        punto_parada = random.uniform(0, 100)
        punto_parada = punto_parada/100
        # Crear varaible que va llenandose hasta llegar al ganadaro con la porbaliidad que le toco
        acumulado = 0
        
        # Ordenar la población acodrde a su valord de peso de mayor a menor
        mapeo_ordenado = sorted(zip(poblacion, pesos), key=lambda x: x[1])
        poblacion = [par[0] for par in mapeo_ordenado]
        pesos = [par[1] for par in mapeo_ordenado]
        
        # recorrer cada indicuido de ls población
        for i, individuo in enumerate(poblacion):
            # Si se llega ala valor de probalidad que le correpodne a un miembro de la población se devulve el resultado
            acumulado += pesos[i]/suma_total
            if acumulado >= punto_parada:
                return individuo
        # si de casualidad no paso se devilve el ultimo, pero que suerte que pase esto.  
        return poblacion[-1]

    def crossover_ox(padre,madre):
        ''' Esta función se encarga de hacer un crosover entre dos padres en la cual
        se obta por preserva simpre la priemra mitada del padre y completar con lo que sobra de la madre o segundo padre'''
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
        # Delvolver el hijo
        return hijo


    def mutacion_swatt(niño, radiacion):
        '''Esta función se encarga de realizar  mutaciones simpre que 
        el nivel de radiación, probabilidad, aleatroio al que se expone la descendencia es mayor 
        al necesacion parta mutar, dado por  el argumento exposicion '''
        if random.random() < radiacion: # Esto esta muy a la novela Un Mundo Feliz
            i, j = random.sample(range(base), 2)
            niño[i], niño[j] = niño[j], niño[i]
        return niño
            
    def proceso_algoritmo_genetico():
        '''Esta función es la que se encarga de relaizar el algorimo genetico a corde a los pasos que este tiene'''
        # Paso 1 crear una población de muchas combinaciones para tener un punto de partida
        # Crear lista vacia con las muchas posibles nuevas poblaciones, Por ejemplo 100
        poblaciones = []
        # Dar numero de individuos para hacer más general el código
        monton = 100
        contador= 0
        while contador <= monton:
            # Empezar a crear cada meimbro con la función de creaar padres
            people = crear_padres()
            if people not in poblaciones:
                poblaciones.append(people)
                contador = contador +1
        
        # Paso 2 seleccioanr el mejor luego de una evolución de varias iteraciones. Aproximadamente 300
        # nuemero de iteraciones. Se escoge ese numero porque si, pero lo puedes cambair en le programa si gustas 
        n_pruebas =300
        # Esto se hace para guardar el tiempo y posibles combinaciones en caso 
        # de haber más de una buena combinación que arroge el valor más pequeño
        posibles_candidatos = []
        menor_peso = float('inf') # Se parte de infinito para luego ir decendiendo. 
        
        valores = []
        for prueba in range(n_pruebas): 
            # Encontrasr el mejor luego de calular el wiTi para cada una de las combinaciones
            poblaciones.sort(key=lambda x: calcular_wi(x)) # Se ordena la lista a corde a al calculo de wiTi de menor a mayor
            mejor_de_momento = poblaciones[0] # Por eso el priemr elemento es  el mejor
            peso_pequeño = calcular_wi(mejor_de_momento)
            
            # Se evalua y guarda en un resgistro el resultado  que arroja un tiempo más pequeño este se cambi y se actualice con varias interacciones. 
            if peso_pequeño < menor_peso:
                menor_peso = peso_pequeño
                # Se guardan la convinación con el menor tiempo
                posibles_candidatos = [] # Sea vacia para el nuevo mejor
                # Se revisa la población
                for candidato in poblaciones:
                    # Si el candidato tiene el tiempo más pequeño se agrega al arreglo
                    if calcular_wi(candidato) == peso_pequeño:
                        posibles_candidatos.append(candidato)
                            
            elif peso_pequeño ==  menor_peso:
                for candidato in poblaciones:
                    if calcular_wi(candidato) == peso_pequeño:
                        # Evaluar si no  esta dentro del arreglo de combinaciones con buenos resultados para ponerlo
                        if candidato not in posibles_candidatos:
                            posibles_candidatos.append(candidato )
                
            # Mostrar mensaje de avance para que el usario sepa que esta passando y no se qued eviendo una pantalla todo el rato y pensando que ya se jodio la máquina. 
            print(f"Se va por la prueba: {prueba +1}. Con el peso:  {menor_peso}")
            # print(f"Las combinaciones son: {posibles_candidatos}")
                

            # Paso tres empezar generar cruces y mutacioens mediante iteracciones para generar una nuevas poblaciones y reprtir el ciclo. 
            
            '''Como se va a usar elistimo se selecciona para guadar en la nueva población lo mejor que dio esta
            Además se usara para guardar nuevos miebros  los que no sean mejores al tiempo peor intermedio de la generación anterior'''
            
            nueva_poblacion = []
            # Añadir lo mejor de antes
            nueva_poblacion.append(mejor_de_momento)
            # Obtener lista de los valores de peso para usarlos depsues en la función ruleta
            pesos_generacion = []
            for individuo in poblaciones:
                # Calcular los pesos 
                wi = calcular_wi(individuo)
                # Realizar inversión de cada miembro de la población, paso para el algotimo de la ruleta. 
                pesos_generacion.append(1.0 / (wi + 1e-6))
            
            # Obtener posición intermedia del arreglo.
            mitad = int(len(poblaciones)/2)
            #mitad = -1
            # Obtener el peor tiempo desde desde el final a la  mitad
            horribles = calcular_wi(poblaciones[-mitad])
            #horribles1 = calcular_wi(poblaciones[0])
            #horribles2 = calcular_wi(poblaciones[-1])
            #print(horribles)
            #print(horribles1)
            #print(horribles2)

            # Empezar a crear el la nueva población de forma que sea similar a la anterior
            # Crear otra igual de un valor igual al monton de indivisuos. 
            while len(nueva_poblacion) < monton:
                # Se crean los nuevos miembros de esa poblaciónes los cuales son los decendientes de padres creados por 
                # una ruleta y luego cruzados para obtenr un hijo. 
                # Ademas después se les expone a radación o mutación con la variable radación para geenra cambios. 
                # Comentario ajeno: La descrición anterior parece como nacen bebes en la novela Un Mundo Feliz. 
                # Crear a los padres
                progenitor1 = ruleta(poblaciones, pesos_generacion) 
                progenitor2 = ruleta(poblaciones, pesos_generacion) 
                evaluacion = comparar_padres_identicos(progenitor1, progenitor2)
                contador_falso = 1
                while contador_falso<1:
                    if evaluacion == "iguales":
                        progenitor1 = ruleta(poblaciones, pesos_generacion) 
                        progenitor2 = ruleta(poblaciones, pesos_generacion)
                    else:
                        contador_falso = 100  
                # Cruzarlos
                resultado = crossover_ox(progenitor1, progenitor2)
                # Mutarlo con una probalidiad de 0.1
                resultado = mutacion_swatt(resultado, 0.1) # Se pone asi por como hablan de los bebes en la novela y no se nos ocurria otro nombre
                
                # Ahora se crea la nueva población con base al crieterio de mejora, repsecto al peor tiempo inetrmedio 
                # De los habitantes anteiores
                
                # Evalaur si el hijo que resulto no esta en la lista de nueva población y cumple con el criterio
                # De tiempo para ponerlo en la nueva población
                if resultado not in  nueva_poblacion:
                    tiempo_producto = calcular_wi(resultado)
                    # Con esto se tiene que solo los hijos aptos se dejan y los que no se descartan por no cumplir para los fines de mejora
                    if tiempo_producto <= horribles:
                        nueva_poblacion.append(resultado) 
            # Hacer a la nueva población,  como la nueva población
            poblaciones = nueva_poblacion
            valores.append(menor_peso)
        
        # Crear grafico donde se ver el compotamiento del algoritmo genetico. 
        eje_x = list(range(1, len(valores) + 1))

        plt.plot(eje_x, valores)
        plt.xlabel("Generación")
        plt.ylabel("Valor (wiTi)")
        plt.title("Cambios con las generaciones del peso acorde a la asignación de empleados")
        plt.grid()
        plt.show()

        
        # Mostrar los resultados
        print()
        print(f"El mejor valor de wiTi obtendio es de {menor_peso}")
        print()
        print("Y se obtiene con las siguientes combinaciones:")
        print()
        contador = 1
        for combinacion_miedo in posibles_candidatos:
            arreglo_miedo = " - ".join(map(str, combinacion_miedo))
            print(f" {contador}:  {arreglo_miedo}")
            contador += 1
    

    #a= ruleta()
    #print(a)
    #b = crossover_ox(a[0],a[1])
    #print(b)
    #c =  mutacion_swatt(b,0.1)
    #print(c)
    #generico = crear_padres()
    #generico2 = crear_padres()
    #a = comparar_padres_identicos(generico, generico2)
    #print(generico)
    #print(generico2)
    #print(a)
    #print(f"El tiempo para el orden de {generico} es {calcular_wi(generico)} s  ")
    #print(f"El tiempo para el orden de {generico2} es {calcular_wi(generico2)} s  ")
    #print(f"El tiempo para el orden de {a[0]} es {calcular_wi(a[0])} s  ")
    
    #print(f"El tiempo para el orden de {a[1]} es {calcular_wi(a[1])} s  ")

    # Llamar al algoritmo genetico como la unica función que se requiere llamar
    proceso_algoritmo_genetico()

    #combinaciones_obtenidas = [
    #  [4, 6, 8, 2, 1, 7, 5, 3],
        #[4, 8, 6, 2, 1, 7, 5, 3],
    # [6, 2, 8, 4, 1, 7, 5, 3],
    #   [8, 2, 4, 6, 1, 7, 5, 3],
    #   [8, 4, 6, 2, 1, 7, 5, 3],
    #   [2, 6, 8, 4, 1, 7, 5, 3],
    #   [2, 4, 8, 6, 1, 7, 5, 3],
    #   [8, 4, 2, 6, 1, 7, 5, 3],
    #   [4, 8, 2, 6, 1, 7, 5, 3],
    #   [4, 2, 8, 6, 1, 7, 5, 3],
    #   [8, 6, 4, 2, 1, 7, 5, 3],
    #   [2, 8, 4, 6, 1, 7, 5, 3],
    #   [8, 6, 2, 4, 1, 7, 5, 3],
    #   [6, 8, 2, 4, 1, 7, 5, 3],
    #   [6, 4, 8, 2, 1, 7, 5, 3],
    #   [6, 8, 4, 2, 1, 7, 5, 3],
    #   [2, 8, 6, 4, 1, 7, 5, 3]
    #]

    #for i, combinacion_terror in enumerate(combinaciones_obtenidas, 1):
    # tiempo = calcular_wi(combinacion_terror)
    # print(f"El tiempo para el orden de {combinacion_terror} es {calcular_wi(combinacion_terror)} s  ")
# Evaluar si algo pasa
except: 
    # En caso de algun problema notificar al usario de forma amable. 
    print()
    print("Se equipoco en el nombre del archivo, no esta en misma carpeta o ese no tiene el formato que corresponde.")
    print("Ponga bien la extensión .xlsx porque el problema es de capa 8 y no esta en el software sino entre el escritorio y la silla") # Esto es una proyectada. 
    print()



