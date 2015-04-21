from math import sqrt, pow
from heapq import heappush, heappop

def closest_box(src,box):
	if (src[0] >= box[0]):
		if (box[1] >= src[0]):
			cX = src[0]
		else:
			cX = box[1]
	else:
		if (box[1] >= box[0]):
			cX = box[0]
		else:
			cX = box[1]

	if (src[1] >= box[2]):
		if (box[3] >= src[1]):
			cY = src[1]
		else:
			cY = box[3]
	else: 
		if (box[3] >= box[2]):
			cY = box[2]
		else:
			cY = box[3]
			
	return (cX,cY)

def distance_fn(dst, src):
   return abs(dst[0] - src[0]) + abs(dst[1] - src[1])	


def find_path(src, dst, mesh):
	path = [] #technically priority queue/heapq
	queue = []
	detail_points = {}
	dist = {}
	prev = {}
	
	start = None
	new_cost = 0.0
	#setup the starting point
	for box in mesh['boxes']:
		if src[0] >= box[0] and src[0] <= box[1] and src[1] >= box[2] and src[1] <= box[3]: #Determine what box source point is in if(x,y) in bounds (x1,x2,y1,y2)
			start = box
			dist[start] = 0.0
	if (start == None): #check to make sure source is valid
		print('Invalid source')
		return [],[] #return empty lists if invalid
	queue = [(dist[start],start,src)] #dist[start] used as priority (heuristic)
	prev[start] = None

	while queue:
		fringe = heappop(queue) #kinda weird syntax, fringe[0] is the dist and fringe[1] is the box, treat fringe[1][0] as box[0]
		if dst[0] >= fringe[1][0] and dst[0] <= fringe[1][1] and dst[1] >= fringe[1][2] and dst[1] <= fringe[1][3]: #same as above, check which box dst is contained in
			dst_box = fringe[1]
			break
		neighbors = mesh['adj'][fringe[1]]
		prev_ = (fringe[2][0],fringe[2][1])

		for next in neighbors:#cycle through adjacency list

			new_xy = closest_box(prev_, next)
			cost = sqrt(pow((prev_[0]-new_xy[0]),2) + pow((prev_[1] - new_xy[1]),2)) #just pure euc dist for cost

			new_cost = dist[fringe[1]] + cost
			if next not in prev or new_cost < dist[next]:
				dist[next] = new_cost
				priority = new_cost  + distance_fn(dst, new_xy) # use linear distance as heuristic
				prev[next] = fringe[1]
				heappush(queue,(priority, next, new_xy))


	if dst[0] >= fringe[1][0] and dst[0] <= fringe[1][1] and dst[1] >= fringe[1][2] and dst[1] <= fringe[1][3]: 
		node = fringe[1]
		while node != start:
			path.append(node)
			node = prev[node]
		path.reverse()
		prevNode = src
		for box in path:
			line = closest_box(prevNode, box)
			detail_points[box] = (prevNode,line)
			if box != dst_box:
				prevNode = (line)
		detail_points[dst_box] = (prevNode,dst)
		return detail_points.values(), prev.keys()
	else:
		print ('No such path!')
		return detail_points.values(), prev.keys()
