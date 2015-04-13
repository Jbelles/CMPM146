import random

def think(state, quip):
	current_moves = state.get_moves()
	curr_score = state.get_score()[state.get_whos_turn()]
	
	for move in current_moves: #look for moves that score
		test = state.copy()
		test.apply_move(move)
		if test.get_score()[state.get_whos_turn()] > curr_score:
			return move
			#this just returns the first move it comes across that scores a point
	return random.choice(state.get_moves())#otherwise just random if all = score