import csv 
import math
import sys

def build_path(node, previous):
		path = [node]
		while node in list(previous.keys()):
			node = previous[node]
			path.insert(0, node)
		return path

def solve(start, end, h, d):
	if(start not in list(d.keys()) or end not in list(d.keys())):
		print(f"Error: Start:{start} or End:{end} node doesn't exist in nodes:{list(d.keys())}")
		return None

	print(f"{start}->{end}")
	schedule = [start]
	previous = dict()
	g = dict()
	f = dict()
	for ele in [node for node in d.keys()]:
		g[ele] = math.inf
		f[ele] = math.inf
	g[start]=0
	f[start]=h[start][end]
	it = 0
	while(len(schedule)!=0):
		print("IT ",it," --")
		it+=1
		print(f"f:{f}")
		print(f"g:{g}")
		print(f"schedule:{schedule}")
		
		min_f = math.inf
		min_node = None
		print(f"min_node = min v")
		for evalf in schedule:
			print(f"\tf[{evalf}]:{f[evalf]}")
			
			if f[evalf] < min_f:
				min_node = evalf 
				min_f = f[evalf]
			print(f"\t\tmin_node:{min_node}")

		if(min_node==end):
			return build_path(min_node,previous)
		print(f"min_node:{min_node}")
		schedule.remove(min_node)

		for adj in list(d[min_node].keys()):
			evalg = g[min_node] + d[min_node][adj]
			print(f"\t\tv {evalg}:evalg = {g[min_node]}:g[{min_node}] + {d[min_node][adj]}:d[{min_node}][{adj}]")
			print(f"\tadj:{adj} - {evalg}:evalg <comp> {g[adj]}:g[{adj}]")
			if evalg < g[adj]:
				previous[adj]=min_node
				g[adj]=evalg
				f[adj]=evalg + h[adj][end]
				print(f"\t\tupdated - f[{adj}]:{f[adj]} = {h[adj][end]}:h[{adj}][{end}] + {g[adj]}g[{adj}]")

				if adj not in schedule:
					schedule.append(adj)

		print(f"previous:{previous}")
		print(f"new schedule:{schedule}")
	print(f"Unreachable Nodes")
	return None
def main(argv):
	if (len(argv)<3):
		print("Usage: $astar [start] [end]")
		return 1

	if (sys.argv[1]):
		start_at = int(sys.argv[1])
	if (sys.argv[2]):
		end_at = int(sys.argv[2])

	heuristics_path = "data/heuristics.csv"
	distances_path = "data/real-distances.csv"

	csvh = open(heuristics_path)
	grid1 = list(csv.reader(csvh))
	print(f"Hcsv:\n\t{grid1}")

	csvd = open(distances_path)
	grid2 = list(csv.reader(csvd))
	print(f"Dcsv:\n\t{grid2}")

	d = dict()
	for i, row in enumerate(grid2):
		d[i+1] = dict()
		for j, col in enumerate(row):
			if(col!='0.'):
				d[i+1][j+1] = float(col)
	print(f"D:\n\t{d}")
	heuristics = dict()
	for i, row in enumerate(grid1):
		heuristics[i+1] = dict()
		for j, col in enumerate(row):
			#if(col!='0.'):
			heuristics[i+1][j+1] = float(col)
	print(f"H:\n\t{heuristics}")

	path = solve(start_at, end_at, heuristics, d)
	if(path):
		print("bestpath:\n\t",path)
		print("cost:\n")
		cost = 0
		for i in range(0,len(path)-1):
			cost += d[path[i]][path[i+1]]
		print(f"\t{cost}")
		

if __name__ == "__main__":
    main(sys.argv)

