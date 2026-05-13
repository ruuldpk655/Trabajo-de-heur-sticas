'''
        Universidad de Costa Rica
            Sede Occidente  

        Escuela de Ingeniería Industrial  

    Modelos Estocásticos y Heurísticos para la Industria

    Caso: Problema del agente viajero
        
            Estudiantes:
        Melany Vargas Blanco C28100 
        Britny Mendoza Murillo C14736
        Raúl Evelio Fernández Vargas C02975  
        Joseph Alpizar Alpizar C00240

        Profesor: Ronny Pacheco Segura 
 
                    I-2026
'''


# Importar librerías para la realización del trabajo.
import pandas as pd
import matplotlib.pyplot as plt
import random

'''Para este código se tiene que se esocogio priemero poner las funciones que se encargan de hacer el algorimo genetico como: la mutación 
el toerneo y  el crossover'''

# Crear función de claculo de peso total del drone y suma de valores
def calcular_wi(orden, datos_matriz):
    """Esta función se encarga  de calcular el valor clinico con la la infomaciónd e las columnas del 
    archivo Exel que debe arbirse cuando se ejecute este códido"""
    # Variables vacias para sumar el peso el valor clinico 
    peso= 0
    valor_clinico= 0
    pedido = []
    # Recorrer lista de los productos que se seleccionarón para calcular el valor clinico
    for objeto in orden:
        fila = objeto - 1 
        # Obtener filas con los pesos y las valores clínicos
        masa = datos_matriz[fila, 2]
        valor = datos_matriz[fila, 3]
        
        # Evaluar que la suma de las cosas no sea mayor a 45 
        if peso + masa <= 45:
            # Sumar masas hasta que estas sean 45
            peso += masa
            # Sumar los valores clinicos de esos productos
            valor_clinico += valor
            # Agregar productos al pedido que enviara el dron
            pedido.append(objeto)
        else:
            # Si de da que ya esta en 45 se se envia mas
            break
    
    # Devolver cuales son los productos a enviar, el valor clinico y el peso en kg
    return valor_clinico, pedido, peso

# Crear función para hacer crossover 
def crossover_ox(padre, madre):
    ''' Esta función se encarga de hacer un crosover entre dos padres en la cual
    se obta por preservar simpre la priemera mitada del padre y completar con lo que sobra de la madre o segundo padre'''
    # Obtner la mitad
    extension = len(padre)
    mitad = int(extension / 2) 
    # Crear hijo 
    hijo = padre[:mitad]
    # Los sobrantes son los elemntos que se completan con la madre
    sobrantes = [elemento for elemento in madre if elemento not in hijo]
    # Poner sobrantes en hijos
    hijo.extend(sobrantes)
    # Devolver hijo
    return hijo

# Crear función para hacer mutación
def mutacion_swatt(niño, radiacion):
    '''Esta función se encarga de realizar  mutaciones simpre que 
        el nivel de radiación, probabilidad, aleatroio al que se expone la descendencia es mayor 
        al necesacion parta mutar, dado por  el argumento exposicion '''
    if random.random() < radiacion: # Entiendase radiación como algo que muta o en este caso la porbalididad de mutación. Se puso ese nombre porque parecía bonito. 
        i, j = random.sample(range(len(niño)), 2)
        niño[i], niño[j] = niño[j], niño[i]
    return niño

def torneo(poblacion, valor, k):
    """Esta función se encarga de hacer la selección de los elelmntos  de la poblasción y ponerlos a compertir para decidir el mejor """
    peleadores = random.sample(range(len(poblacion)), k)
    # Elegir peleadores del toerno, ponerlos a competir y encontrar el mejor 
    ganador = peleadores[0]
    for participante in peleadores:
        if valor[participante] > valor[ganador]:
            ganador = participante
    return poblacion[ganador]

# --- ALGORITMO GENÉTICO PRINCIPAL ---

def proceso_algoritmo_genetico(base_datos):
    """"Hacer uso del algoritmo genetico de mejora para hayar  la combinación que 
    puede llevar el drone con nmayor valor medico y en el limite maximo de peso. """
    
    """"Muchas variables y funciones tienen nombres extraños porque este codigo tiene 
    su origen de un problema de asginación al cual se le hicierón cambios Igualemnte se explcia con detalle
    que es cada variable
    """
    # Obtener la base de datos que se lee de un Excel con la información
    datos_matriz = base_datos.values
    # Obtener el numero de los items de los productos medicos
    trabajadores = base_datos.iloc[:, 0].to_list()             
    # Obtener la cantidad total de produtos
    base = len(trabajadores)
    # Número de indivudiso de la población 
    monton = 100
    # Cantidad total de generacioenes a probar
    n_pruebas = 1000
    # Crear la población a partir de los productos medicos y su cantidad
    poblaciones = [random.sample(trabajadores, k=base) for _ in range(monton)]
    
    # Definir variables de iniciación para hacer prueba de si algo es mas grande que lo anteior y asi ir mejorando. 
    mayor_valor_alcanzado = -1.0
    # Guadar mejor solución de momento
    mejor_solucion_global = []
    # Esto es para guardar en una lista de valores como avanza la mejora y con ello hacer un grafico
    valores_grafico = []

    # Iterar a traves de las generaciones
    for prueba in range(n_pruebas):
        # Evaluación: Obtenemos el mejor valor clinico de la población
        resultados_evaluacion = [calcular_wi(ind, datos_matriz) for ind in poblaciones]
        mejor_población  = [resultados[0] for resultados in resultados_evaluacion]
        
        # Hallar el mejor de la generación
        max_valor = max(mejor_población)
        if  max_valor > mayor_valor_alcanzado:
            mayor_valor_alcanzado =  max_valor 
            mejor_solucion_global = poblaciones[mejor_población.index( max_valor )][:]

        # Crear nueva población
        nueva_poblacion = [mejor_solucion_global] # Elitismo
        while len(nueva_poblacion) < monton:
            # Hacer padres con el torneo
            p1 = torneo(poblaciones, mejor_población, k=5)
            p2 = torneo(poblaciones,mejor_población, k=5)
            # Hacer crossover con los padres
            hijo = crossover_ox(p1, p2)
            # Mutar al hijo con una probalidad de 0.2
            hijo = mutacion_swatt(hijo, 0.2)
            # Añadir al hijo a la nueva población  si este no esta
            if hijo not in nueva_poblacion:
                     nueva_poblacion.append(hijo)
        
        # Hacer nueva población 
        poblaciones = nueva_poblacion
        # Añadir esos valores del grafico
        valores_grafico.append(mayor_valor_alcanzado)
        
        # Mostrar resultado de momento 
        print(f"Mayor valor de peso de momento por la generación {prueba +1} es: {mayor_valor_alcanzado} ")
        
        
    # --- RESULTADOS FINALES  ---
    valor_final, items, peso_final = calcular_wi(mejor_solucion_global, datos_matriz)
    
    nombres_productos = []
    for identificador in items:
        nombre = base_datos.iloc[identificador - 1, 1] 
        nombres_productos.append(nombre)
    # Mostrar resultados
    print()
    print(f"Resultados finales".upper())
    print()
    print(f"Valor clíninico total: {valor_final}")
    print()
    # Peso final 
    print(f"Peso Total que transporta el dron: {peso_final} Kg ")
    print()
    print()
    contador_falso = 1
    
    print("Los productos que transporta el dron son los siguientes:")
    print()

    # Esto es para dar formato de lista 
    contador_falso = 1
    # El nombre del producto (columna 1)
    for i in range(len(items)):
        # Identidicar posiciones
        id_item = items[i]
        posicion = items[i]
        # Nombre del producto
        medicina = nombres_productos[i]
        # Obtener valor y peso
        peso_u = datos_matriz[id_item - 1, 2]  
        valor_u = datos_matriz[id_item - 1, 3] 
        # Mostrar lista de productos
        print(f"{contador_falso}. {medicina}. Peso: {peso_u} kg.  Valor: {valor_u}")
        contador_falso += 1
        
        
    # Crear cromosoma
    cromo = [0] * base
    for numero in items:
        cromo[numero- 1] = 1
        
    print()
    print(f"Con el siguiente cromosoma binario de {base} posiciones")
    print()
    print(cromo)
    
        
    
    
    plt.plot(valores_grafico, color="green")
    plt.title("Comportamiento del valor clínico durante las generaciones")
    plt.xlabel("Generaciones")
    plt.ylabel("Valor Clínico")
    plt.grid(True)
    plt.show()

# Llamar a las funciones que relaizan el proceso

try:
    # Pedir al usuario la infoamción para trabajar desde un Excel
    nombre = input("Ingrese el nombre del archivo (.xlsx) con la infomación de los produtos a trasportar con el dron: ")
    base_datos_fina = pd.read_excel(nombre)
    proceso_algoritmo_genetico(base_datos_fina)
except Exception as e:
    # En caso de algun problema notificar al usario de forma amable. 
    print(e)
    print("Se equivoco en el nombre del archivo, no esta en misma carpeta o ese no tiene el formato que corresponde al numero que puso.")
    print()
    print("Tambien es posible que no pusiera algo que es un número del 1 al 4 cuando fue lo unico que se le pidio hacer eso. ")
    print()
    print("Ponga bien la extensión .xlsx y el número, porque el problema es de capa 8 y no esta en el software sino entre el escritorio y la silla.".upper()) 
    print()
    print("Por ello Usuario lea bien por favor".upper())
    print()

