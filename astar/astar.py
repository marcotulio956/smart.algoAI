import csv 
import math

csvh = open("data/heuristics.csv")
grid1 = list(csv.reader(csvh))
print(f"H: \n{grid1}")

csvd = open("data/real-distances.csv")
grid2 = list(csv.reader(csvd))
print(f"D: \n{grid2}")

start_at = 6
end_at = 13

def solve(start, end, h, distances):
	graph = dict()
	for i, row in enumerate(distances):
		graph[i] = []
		for j, col in enumerate(row):
			if(col!='0.'):
				graph[i].append((j, col))
				print(f"G:\n\t{graph}")

	visited = []
	schedule = [start]
	g = dict()
	f = dict()
	g[start] = 0
	while(len(schedule)!=0):
		node = schedule.pop()
		for tup in graph[node]:
			f[tup[0]] = float(h[node][tup[0]]) + g[node]
			print(f"fn:{f}")
		leastf = math.inf
		for tup in graph[node]:
			if f[tup[0]] < leastf:
				leastf = f[tup[0]]
		print(f"leastf:{leastf}")

		break
solve(start_at, end_at, grid1, grid2)

