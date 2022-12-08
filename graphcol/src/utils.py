from src.graph import Grafo
import random

def generateGraph (auto_gen, auto_gen_graph_size, generateGraphFunc: callable = None):
    ''' 
        Gerando o grafo automaticamente, ou manualmente (devemos passar uma funcao que retorna um grafo, como a manual_graph_population_img1)
    '''
    if not auto_gen:
        '''
            Gerando um grafo manualmente
        '''
        graph = Grafo()
        graph = generateGraphFunc(graph)
    else:
        '''
            Gerando um grafo aleatoriamente com tamanho pre-definido (tamanho = num vertices)
        '''
        n = auto_gen_graph_size
        auto_graph = []
        for i in range(n):
            vertex = []
            for j in range(n):
                vertex.append(random.randint(0, 1))
            auto_graph.append(vertex)
        for i in range(n):
            for j in range(0, i):
                auto_graph[i][j] = auto_graph[j][i]
        for i in range(n):
            auto_graph[i][i] = 0
        # Traduzindo o grafo para o padrao utilzado
        graph = Grafo()
        for i in range(n):
            graph.adiciona_vertice(i+1, str(i+1))
        for i in range(n):
            for j in range(n):
                if auto_graph[i][j] == 1:
                    graph.adiciona_aresta(i+1, j+1)
    return graph

def print_population(population, print_vertex: bool = True):
    for i, individual in enumerate(population):
        print(f"individuo {i+1}:")
        individual.print_graph(print_vertex)
        print("")