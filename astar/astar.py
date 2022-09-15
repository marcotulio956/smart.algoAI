import csv 
import math
import sys

def solve(start, end, h, d):
	if(start not in list(d.keys()) or end not in list(d.keys())):
		print(f"Error: Start:{start} or End:{end} node doesn't exist in nodes:{list(d.keys())}")
		return None

	print(f"{start}->{end}")
	visited = [] # closed list
	schedule = [start] # open list
	f = dict()
	g = dict()
	f[start]=g[start]=0
	f[end]=g[end]=0
	for ele in [node for node in d.keys()]:
		g[ele] = 0
	it = 0
	while(len(schedule)!=0):
	# for it in range(0,10):
		print("IT ",it," --")
		it+=1
		# known.update(set(d[node].keys()))
		# print(f"known:{known}")
		print(f"f:{f}")
		print(f"g:{g}")
		node = schedule[0]
		for evalf in schedule:
			if f[evalf] < f[node]:
				node = evalf 
		schedule.remove(node)
		visited.append(node)
		print(f"node:{node}")
		print(f"expan:{d[node]}")
		print(f"visited:{visited}")

		if(node == end):
			print("end\nPATH:")
			previousnode = end
			backtrack = [previousnode]
			while(previousnode != start):
			# for i in range(0,5):
				print("pn",previousnode)
				for previous in d[previousnode]:
					print("\tp",previous)
					if previous in visited and not previous in backtrack:
						previousnode = previous
						backtrack.append(previousnode)
						if(previousnode == start):
							break
						print("\tbt",backtrack)
						continue
			return backtrack[::-1]
		
		for evaln in d[node]:
			print(f"evaln:{evaln}")
			if evaln in visited:
				continue
			g[evaln] = g[node] + d[node][evaln]
			f[evaln] = g[evaln]
			if (evaln!=end):
				estimative = h[evaln][end]
				f[evaln] += estimative
				print(f"\tf({evaln}) = {g[evaln]} g + {h[evaln][end]} h")
			print(f"\tf({evaln}) = {f[evaln]}")
			if True in [snode == evaln and g[evaln] > g[snode] for snode in schedule]:
				continue
			
			schedule.append(evaln)

		print(f"schedule:{schedule}")

def main(argv):
	if (len(argv)<3):
		print("Usage: $astar [start] [end]")
		return 1

	if (sys.argv[1]):
		start_at = int(sys.argv[1])
	if (sys.argv[2]):
		end_at = int(sys.argv[2])

	heuristics_path = "data/heuristics2.csv"
	distances_path = "data/real-distances2.csv"

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
			if(col!='0.'):
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

