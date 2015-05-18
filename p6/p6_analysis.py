from p6_game import Simulator

ANALYSIS = {}

def analyze(design):
    sim = Simulator(design)
    init = sim.get_initial_state()

    queue = []
    prev = []

    state = sim.get_initial_state()
  
    queue.append((state, [state]))
    prev.append(state)
    
    while queue:
        (prevstate, path) = queue.pop(0)
        for next in sim.get_moves():
            next_state = sim.get_next_state(prevstate, next)
            if (next_state not in ANALYSIS and next_state is not None):
                if next_state not in prev:
                    ANALYSIS[next_state] = path
                    queue.append((next_state, path + [next_state]))
                    prev.append(next_state)
    
    # TODO: fill in this function, populating the ANALYSIS dict

def inspect((i,j), draw_line):
    found = False
    for next in ANALYSIS.keys():
        if i is next[0][0] and j is next[0][1]:
            pos, abil = next
            path = ANALYSIS[next]
            for n in range(len(path) - 1):
                found = True
                draw_line(path[n][0], path[n+1][0], color_obj=path[n][1])
            draw_line(path[-1][0], (i,j), color_obj=path[-1][1])
            break
    if not found:
        print "No Path Available"