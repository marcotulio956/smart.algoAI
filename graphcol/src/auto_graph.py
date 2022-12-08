import csv
from src.graph import Grafo 

d = { n-96:chr(n) for n in range(97,123) } # alfabeto

def div(n):
    if ((n%26) == 0 and n>26):
        return int2str_beautify(n//26 - 1)
    elif (n//26) <= 0:
        return ''
    elif n == 26:
        return 'z'
    elif (n//26) in d:
        return d[n//26]
    else:
        return int2str_beautify(n//26)

def mod(n):
    if n<=0:
        return ''
    elif ((n%26) == 0 and n>26):
        return 'z'
    elif (n%26)<=0:
        return ''
    else:
        return d[n%26]

def int2str_beautify(n):
    res_div = div(n)
    res_mod = mod(n)
    return (res_div + res_mod)

def auto_graph_readfile(path):
	csvfile = open(path)
	mtx = list(csv.reader(csvfile))
	print(f"csv:\n\t{mtx}")

	graph = Grafo()

	for i in range(0, len(mtx)):
		graph.adiciona_vertice(
			i, int2str_beautify(i+1), mtx[i][0]
		)
		print(graph.vertices[i])

	for i in range(0, len(mtx)):
		for j in range(1, len(mtx[i])):
			#print(f"> {i}{j}: {mtx[i][j]}")
			if(mtx[i][j] == '1'):
				print(f"add {i}->{j-1}: {mtx[i][j]}")
				graph.adiciona_aresta(i, j-1)

	return graph

def main(argv):
	if (len(argv)<2):
		print("Usage: $auto_graph [path/file.csv]")
		return 1

	if (sys.argv[1]):
		path = sys.argv[1]

	print(path)
	graph = auto_graph_readfile(path)
	graph.print_graph()
	graph.visualize()

if __name__ == "__main__":
	import sys
	main(sys.argv)