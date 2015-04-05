from p1_support import load_level, show_level
from math import sqrt
from heapq import heappush, heappop

def dijkstras_shortest_path(src, dst, graph):
	frontier = [] #Declare Heapq element frontier
	heappush(frontier, src)
	came_from = {}
	cost_so_far = {}
	came_from[src] = None
	cost_so_far[src] = 0

	while frontier:
	   current = heappop(frontier)
	   if current == dst:
		  break

	   x, y = current
	   for dx in [-1,0,1]:
		for dy in [-1,0,1]:
		  next = (x + dx, y + dy) 
		  new_cost = cost_so_far[current] + sqrt(x*x+y*y)
		  if next not in cost_so_far or new_cost < cost_so_far[next]:
			cost_so_far[next] = new_cost
			priority = new_cost
			heappush(frontier, next)
			came_from[next] = current

	if current == dst:
		path = []
		while current:
			path.append(current)
			current = prev[current]
		path.reverse()
		return path
	else:
		return []


def test_route(filename, src_waypoint, dst_waypoint):
	level = load_level(filename)

	show_level(level)

	src = level['waypoints'][src_waypoint]
	dst = level['waypoints'][dst_waypoint]

	path = dijkstras_shortest_path(src, dst, level)

	if path:
		show_level(level, path)
	else:
		print "No path possible!"

if __name__ ==  '__main__':
	import sys
	_, filename, src_waypoint, dst_waypoint = sys.argv
	test_route(filename, src_waypoint, dst_waypoint)
