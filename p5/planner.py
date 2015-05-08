import json
from collections import namedtuple
from math import sqrt
from heapq import heappush, heappop

with open('Crafting.json') as f:
    Crafting = json.load(f)

total_cost = 0
plan = None
items = {}
inventory = []
Recipe = namedtuple('Recipe', ['name', 'check', 'effect', 'cost'])

def set_goal(inventory):
    temp_goal = list(inventory)
    for each in Crafting['Goal']:
        temp_goal[items[each]] = Crafting['Goal'][each]
    return tuple(temp_goal)

def goal_check(state, goal):
    for i in range(len(state)):
        if state[i] < goal[i]:
            return False
    print "Goal Found"
    return True

def make_initial_state(inventory):
    i = 0
    initial_state = inventory
    for item in Crafting['Items']:
        items[item] = i
        i += 1
        initial_state.append(0)
    initial_state = list(inventory)
    return initial_state

def make_checker(rule):
    # this code runs once
    requires = None
    consumes = None
    if 'Requires' in rule:
        requires = rule['Requires']
    if 'Consumes' in rule:
        consumes = rule['Consumes']

    def check(state):
        # this code runs millions of times
        if consumes:
            for i in consumes:
                if state[items[i]] < consumes[i]:
                    return False
        if requires:
            for i in requires:
                if state[items[i]] < 1:
                    return False
        # if the above conditions are satisfied, return true.
        return True

    return check

def make_effector(rule):
    # sets up the effector that will effect the state when called.
    produces = rule['Produces']
    consumes = None
    # check to see if the recipe consumes anything
    if 'Consumes' in rule:
        consumes = rule['Consumes']

    def effect(state):
        # this code runs millions of times
        # copy current state
        next_state = list(state)
        if consumes:
            for i in consumes:
                next_state[items[i]] -= consumes[i]
        for i in produces:
            next_state[items[i]] += produces[i]

        return next_state

    return effect



def search(recipes, initial_state, goal, is_goal, limit, heuristic):
    queue = []
    prev = {}
    dist = {}
    disc = []
    recipe_name = {}
    curr_state = list(initial_state)

    recipe_name[tuple(curr_state)] = ""
    prev[tuple(curr_state)] = None
    dist[tuple(curr_state)] = 0

    while not is_goal(curr_state, goal):
        for recipe in recipes:
            # For each possible recipe from our current state:
            if recipe.check(curr_state):
                # Use the recipe, then update distance and previous nodes.
                new_state = tuple(recipe.effect(curr_state))
                if new_state not in disc:
                    prev[new_state] = tuple(curr_state)
                    dist[new_state] = dist[tuple(curr_state)] + recipe.cost
                    heappush(queue, (dist[new_state], new_state))
                    disc.append(new_state)
                    recipe_name[tuple(curr_state)] = recipe.name

                elif dist[new_state] > dist[curr_state] + recipe.cost:
                    # replace value if we have found a 'faster' route
                    prev[new_state] = tuple(curr_state)
                    dist[new_state] = dist[curr_state] + recipe.cost
                    # recipe_name[tuple(curr_state)] = recipe.name
        curr_state = heappop(queue)[1]
    print "new state", curr_state

    total_cost = dist[curr_state]

    path = []
    recipe_name[curr_state] = "Goal"

    while curr_state != None:
        # append recipe names
        path.append(recipe_name[curr_state])
        # append states
        #path.append(curr_state)
        print curr_state
        curr_state = prev[curr_state]
    #print path
    path.append("Start")
    #print items

    for i in range(len(path)):
        print[path[len(path)-i-1]]


    #return an array of points
    return total_cost, path
# End A*


def main():
    state = make_initial_state(inventory)
    goal = set_goal(state)
    all_recipes = []
    for name, rule in Crafting['Recipes'].items():
        checker = make_checker(rule)
        effector = make_effector(rule)
        recipe = Recipe(name, checker, effector, rule['Time'])
        all_recipes.append(recipe)


    print search(all_recipes, state, goal, goal_check, 20, None)

    # print items
    for i in range(100):
        for recipe in all_recipes:
            if recipe.check(state):
                state = recipe.effect(state)
        # print state
    # print items

# End def main
main()