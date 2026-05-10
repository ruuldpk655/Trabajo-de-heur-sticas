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
    datos_matriz = base_datos.values
    
    def calcular_wi(orden): # (1,2, 3, 4 5, 6, 7, 8 )
        '''Crear  función para calular wi.Ti'''
        tiempo_acumulado = 0
        suma_witi = 0
        
        # Un solo bucle para procesar todo: Ci, Ti y WiTi
        for job_idx in orden:
            # Ajustamos el índice (suponiendo que 'orden' tiene valores de 1 a 30)
            fila = job_idx - 1 
            
            # Acceso directo por posición (p=col 1, d=col 3, w=col 4)
            p = datos_matriz[fila, 1]
            d = datos_matriz[fila, 3]
            w = datos_matriz[fila, 4]
            
            # 1. Calcular Ci (Tiempo acumulado)
            tiempo_acumulado += p
            
            # 2. Calcular Ti (Tardanza) y 3. Sumar Wi*Ti de inmediato
            # max(0, Ci - d) asegura que si termina antes, la tardanza sea 0
            tardanza = tiempo_acumulado - d
            if tardanza > 0:
                suma_witi += tardanza * w  
        return suma_witi
    
    # Crear función para generar el número de padres 
    def crear_padres():
        """Es función tiene el proposito de crear posibles combinaciones laeatorias de trabajadores que van desd el 1 hasta 
        el número total a asignar que se reuqiera de estos"""
        distribucion= random.sample(trabajadores, k = base)
        # Devolver distribución
        return distribucion
    
    # Crear función para hacer crossover     
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

    # Crear función para hacer mutación
    def mutacion_swatt(niño, radiacion):
        '''Esta función se encarga de realizar  mutaciones simpre que 
        el nivel de radiación, probabilidad, aleatroio al que se expone la descendencia es mayor 
        al necesacion parta mutar, dado por  el argumento exposicion '''
        if random.random() < radiacion: # Esto esta muy a la novela Un Mundo Feliz
            i, j = random.sample(range(base), 2)
            niño[i], niño[j] = niño[j], niño[i]
        return niño
    
    # Crear función para torneo
    def torneo(poblacion, distancias, k):
        """Esta función se encarga de hacer la selección de los elekntos d ela poblasción y poner los a compertir para decidir el mejor """
        # Elegir a los peleaodres del  Tenkaichi Budōkai numero 21
        peleadores = random.sample(range(len(poblacion)), k)
        # Encontrra cual es Goku en esos participantes
        # Ver el indice del priemer elemento de los peleadores
        ganador = peleadores[0]
        # Recorrer todos los peledores hasta hayar el que tiene mayor nivel de poder
        for participante in peleadores:
            if distancias[participante] < distancias[ganador]:
                ganador = participante
        # 3. Devolver el Maestro Roshi del torneo
        return poblacion[ganador]


    def proceso_algoritmo_genetico():
        """Hacer uso del algoritmo genetico de mejora para hayar cual es la ruta más corta 
     para el ajente viajero. Con una población de 100 y 1000 generaciones  """
    
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
        
        # Seleccioanr el mejor luego de una evolución de varias iteraciones. Apromadamente 1000
        # nuemro de iteracioens 
        n_pruebas =1000
        # Esto se hace para guardar el tiempo y posibles combinacioens en caso 
        # de haber más de una buena combinación que arroge el valor más pequeño
        posibles_candidatos = []
        menor_peso = float('inf') # Se parte de infinito para luego ir decendiendo. 
        # Lista vacia para depseus realizar el gráfico
        valores = []
        for prueba in range(n_pruebas): 
            # Caluclar el valor de los pesos. 
            distancias_poblacion = [calcular_wi(ind) for ind in poblaciones]
            
            # Encontrar el menor peso de momento
            menor_peso_gen = min(distancias_poblacion)
            indice_mejor = distancias_poblacion.index(menor_peso_gen)
            mejor_de_momento = poblaciones[indice_mejor]

            # Actualizar cual es el mejor de momento
            if menor_peso_gen < menor_peso:
                menor_peso = menor_peso_gen
                posibles_candidatos = [mejor_de_momento[:]]
            elif menor_peso_gen == menor_peso:
                if mejor_de_momento not in posibles_candidatos:
                    posibles_candidatos.append(mejor_de_momento[:])

            print(f"Se va en generación: {prueba + 1}. Con el  menor peso wiTi: {menor_peso} de momento")
            
            # Crear la nueva población
            nueva_poblacion = []
            nueva_poblacion.append(mejor_de_momento) # Elitismo
            # Crar una nueva población igual de grande que la primera
            while len(nueva_poblacion) < monton:
                # Realizar la escogencia de padres
                progenitor1 = torneo(poblaciones, distancias_poblacion, k=3)
                progenitor2 = torneo(poblaciones, distancias_poblacion, k=3)
                # Hacer el crossover y la mutación
                resultado = crossover_ox(progenitor1, progenitor2)
                resultado = mutacion_swatt(resultado, 0.2)
                # Hacer toda la población distinta
                if resultado not in nueva_poblacion:
                    nueva_poblacion.append(resultado)
            
            # Reemplazar población vieja con la nueva
            poblaciones = nueva_poblacion
            valores.append(menor_peso)
        # Variable con numero de genraciones para el grafico
        x = list(range(1, len(valores) + 1))

        # Mostrar los resultados
        print()
        print(f"El valor menor de peso wiTi obtendio es de {menor_peso}.")
        print()
        print("Y se obtiene con la sigueinte combinación:")
        print()
        contador_1 = 1
        for combinacion_miedo in posibles_candidatos:
            arreglo_miedo = " - ".join(map(str, combinacion_miedo))
            print(f" {contador_1}:  {arreglo_miedo}")
            contador_1 += 1
        # Realizar gráfico
        plt.plot(x, valores, color = "purple")
        plt.xlabel("Generaciones")
        plt.ylabel("Peso total wiTi")
        plt.title("Cambio con las generaciones")
        plt.grid()
        plt.show()
        
    # Llamar al algoritmo genetico como la unica función que se requiere llamar
    proceso_algoritmo_genetico()

except: 
      # En caso de algun problema notificar al usario de forma muy amable. 
    print()
    print("Se equivoco en el nombre del archivo, no esta en misma carpeta o ese no tiene el formato que corresponde")
    print()
    print("Ponga bien la extensión .xlsx, porque el problema es de capa 8 y no esta en el software sino entre el escritorio y la silla.".upper()) 
    print()
    print("Por ello Usuario lea bien por favor, nada le cuesta".upper())
    print()




