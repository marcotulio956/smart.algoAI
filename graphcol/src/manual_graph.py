def manual_graph_population_img1(graph):        
    graph.adiciona_vertice(1, "A")
    graph.adiciona_vertice(2, "B")
    graph.adiciona_vertice(3, "C")
    graph.adiciona_vertice(4, "D")
    graph.adiciona_vertice(5, "E")
    graph.adiciona_vertice(6, "F")
    graph.adiciona_vertice(7, "G")
    graph.adiciona_vertice(8, "H")
    graph.adiciona_vertice(9, "I")
    graph.adiciona_vertice(10, "J")

    graph.adiciona_aresta(1, 2)
    graph.adiciona_aresta(1, 3)
    graph.adiciona_aresta(1, 4)

    graph.adiciona_aresta(2, 1)
    graph.adiciona_aresta(2, 5)
    graph.adiciona_aresta(2, 9)

    graph.adiciona_aresta(3, 1)
    graph.adiciona_aresta(3, 7)
    graph.adiciona_aresta(3, 8)

    graph.adiciona_aresta(4, 1)
    graph.adiciona_aresta(4, 6)
    graph.adiciona_aresta(4, 10)

    graph.adiciona_aresta(5, 2)
    graph.adiciona_aresta(5, 6)
    graph.adiciona_aresta(5, 8)

    graph.adiciona_aresta(6, 4)
    graph.adiciona_aresta(6, 5)
    graph.adiciona_aresta(6, 7)

    graph.adiciona_aresta(7, 3)
    graph.adiciona_aresta(7, 6)
    graph.adiciona_aresta(7, 9)

    graph.adiciona_aresta(8, 3)
    graph.adiciona_aresta(8, 5)
    graph.adiciona_aresta(8, 10)

    graph.adiciona_aresta(9, 2)
    graph.adiciona_aresta(9, 7)
    graph.adiciona_aresta(9, 10)

    graph.adiciona_aresta(10, 4)
    graph.adiciona_aresta(10, 8)
    graph.adiciona_aresta(10, 9)

    return graph