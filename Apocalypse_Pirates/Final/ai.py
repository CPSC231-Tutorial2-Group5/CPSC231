#################################################################################################
#T2G5 Final Project Submission                                                                  #
#By: The Apocalypse Pirates; Ahmed Elbannan, Hilmi Abou-Saleh, Ahmad Turkmani, Nasir Osman      #
#################################################################################################
#The AI module holds the tree related to the moves it should make.                              #
##Add more info                                                                                 #
#################################################################################################

import random
import grid
#import important ports

KNIGHT_MOVES = [[2,1], [2,-1], [-2,1], [-2,-1], [1,2], [1,-2], [-1,2], [-1,-2]] # possible knight moves

possible_moves = [] # hmm...
override = [] # once in a lifetime moves

difficulty = 4 # branching factor ~ difficulty


# a small circular node. Found in forests
class node:
	
	def __init__(self):
	
		self.children = list()	# list of children objects
		self.parent = 'none'	# parent object
		self.level = 0			# level on tree
		self.state = 'none'		# which player
		self.dic_human = {}		# human pieces
		self.dic_ai = {}		# ai pieces
	
	### adds a child node, and returns it's value ###
	def add_child(self):
	
		# create the child node
		new_node = node()
		
		# setup the child, add variables, and add it to children
		self.children.append(new_node)
		new_node.parent = self
		new_node.level = self.level + 1
		
		return new_node
	
	### gets the original move to reach this state ###
	def get_ancestor(self, wanted_level):
	
		cur = self # start with me!
		
		# loop through ancestry until we find desired ancestor
		while cur.level > wanted_level or cur.level %2 == 0:
			cur = cur.parent
			
		return cur
	
	### grows the tree to desired degree, and adds them to possible_moves ###
	def grow_tree(self):
		
		if self.state == 'original': # if original (current) board
		
			# add a child and nourish him.
			child = self.add_child() 
			child.dic_human = dict(self.dic_human)
			child.dic_ai = dict(self.dic_ai)
			child.state = 'human'
			child.last_piece = 'none'
			child.grow_tree()
			
		elif self.state == 'human': # if humans go
		
			# get all valid moves
			self.get_valid_moves(self.dic_human, self.dic_ai, self.get_ancestor(1).dic_ai)
			
			# if i have children
			if self.children != []:
				
				for c in self.children: 
					
					c.grow_tree() # grow each of them
					
			else:
					
				possible_moves.append(self) # end of line, so add it here
				
				
		elif self.state == 'ai': # if ai's turn
		
			# get all valid moves
			self.get_valid_moves(self.dic_ai, self.dic_human, self.get_ancestor(1).dic_human) 
			#print(self.children)
			
			# loop thru kids
			for c in self.children:
				
				# finalize turn
				c.dic_human, mb = grid.check_knight(c.dic_human)
				c.dic_ai, mb = grid.check_knight(c.dic_ai)
				c.dic_human, c.dic_ai, b = grid.finalize_move(c.dic_human, c.dic_ai, self.last_piece, c.last_piece)
				
			# get the cream of the crop moves
			best = best_moves(self.children)
			#print(best)
			
			
			for b in best: #loop thru best moves
				
				c = self.children[b] 
				
				won = grid.get_winner(c.dic_human, c.dic_ai) # check win state in future!? Radical dude!
				
				if won == 'none':# no winner in sight...
					
					if self.level < difficulty: # if level not reached
				
						c.grow_tree() # keep on growin
						#print('next_level')
				
					else:
				
						possible_moves.append(c) # were done
						#print('added!', len(possible_moves))
						
				
				elif won == 'ai': # a future where robots rule the world!
					
					override.append(c)  # GET THIS MOVE!!
					
				elif won == 'human': # i...i had a nightmare
					
					return False # quit this whole branch
					
				else: # if draw. Maybe thats all i can hope for
					
					possible_moves.append(c) # maybe it's the best move...
					
			# if I have no children
			if self.children == []:
				
				possible_moves.append(self) # add myself to possible moves
				
			
			
			
			
	### returns all valid moves as nodes		
	def get_valid_moves(self, dic, dic_opp, dic_org):
	
		##### A LOT OF REPEATED CODE IN THIS FUNCTION, HOWEVER THIS IS FOR SPEED. PUTTING IT IN ANOTHER FUNCTIONS SLOWS IT DOWN CONSIDERABLY
		
		for piece in dic:  # go thru dictionary, piece by piece
		
			loc = dic[piece] # get the location of each piece(list)
		
			if loc != 'dead': # if piece isn't dead...
			
				board = grid.recreate_grid(dic) # trying to optimize speed, boards are slighty faster
				opp_board = grid.recreate_grid(dic_opp)
				org_board = grid.recreate_grid(dic_org)

				
				if piece[1] == 'K': # if piece is a knight
				
					for km in KNIGHT_MOVES: 
					
						can_move = True
					
						new_row = loc[0] + km[0]
						new_col = loc[1] + km[1] 
							
						#print(piece, new_row, new_col, loc[0], loc[1])
							
						if 0 <= new_col < grid.GRID_WIDTH and 0 <= new_row < grid.GRID_HEIGHT: # if move is on board
						
							# if move is not overlapping another piece
							if board[new_row][new_col] != grid.b:
								can_move = False
								
							if can_move:								
								
								# add child and teach it what I know
								child = self.add_child()
								child.dic_human = dict(self.dic_human)
								child.dic_ai = dict(self.dic_ai)
								child.last_piece = piece
								child.new_row = new_row
								child.new_col = new_col
								
								# if i am human
								if self.state == 'human':
								
									# update child and switch turn
									child.dic_human[piece] = [new_row, new_col]
									child.state = 'ai'

								elif self.state == 'ai': # if i am ai
								
									# ^^^^^^^^^^^^^^^^^^ (line 180)
									child.dic_ai[piece] = [new_row, new_col]
									child.state = 'human'
			
				elif piece[1] == 'P': # if I am pawn
					
					can_move = False
					
					# which way is forward???
					if piece[0] == 'W': 
						forward = -1
					elif piece[0] == 'B':
						forward = 1
					
					# move ^
					new_row = loc[0] + forward
					new_col = loc[1]
					
					if 0 <= new_col < grid.GRID_WIDTH and 0 <= new_row < grid.GRID_HEIGHT: # if move is on board
						
							# if move is not overlapping another piece 
							if board[new_row][new_col] == grid.b and opp_board[new_row][new_col] == grid.b and org_board[new_row][new_col] == grid.b:
								can_move = True
								
							if can_move:								
								
								child = self.add_child()
								child.dic_human = dict(self.dic_human)
								child.dic_ai = dict(self.dic_ai)
								child.last_piece = piece
								child.new_row = new_row
								child.new_col = new_col
								
								if self.state == 'human':
									child.dic_human[piece] = [new_row, new_col]
									child.state = 'ai'

								elif self.state == 'ai':
									child.dic_ai[piece] = [new_row, new_col]
									child.state = 'human'
					
					can_move = False
					
					# attack ->^				
					new_row = loc[0] + forward
					new_col = loc[1] + 1
					
					if 0 <= new_col < grid.GRID_WIDTH and 0 <= new_row < grid.GRID_HEIGHT: # if move is on board
						
							# if move is not overlapping another piece and there is enemy
							if board[new_row][new_col] == grid.b and opp_board[new_row][new_col] != grid.b and org_board[new_row][new_col] != grid.b:
								can_move = True
								
							if can_move:								
								
								child = self.add_child()
								child.dic_human = dict(self.dic_human)
								child.dic_ai = dict(self.dic_ai)
								child.last_piece = piece
								child.new_row = new_row
								child.new_col = new_col
								
								if self.state == 'human':
									child.dic_human[piece] = [new_row, new_col]
									child.state = 'ai'

								elif self.state == 'ai':
									child.dic_ai[piece] = [new_row, new_col]
									child.state = 'human'	
									
					can_move = False
					
					#for k in board:
						#print(k)
					
					# attack ^<-				
					new_row = loc[0] + forward
					new_col = loc[1] - 1
					
					if 0 <= new_col < grid.GRID_WIDTH and 0 <= new_row < grid.GRID_HEIGHT: # if move is on board
						
							# if move is not overlapping another piece and there is enemy
							if board[new_row][new_col] == grid.b and opp_board[new_row][new_col] != grid.b and org_board[new_row][new_col] != grid.b:
								can_move = True
								
							if can_move:								
								#print('yaya')
								child = self.add_child()
								child.dic_human = dict(self.dic_human)
								child.dic_ai = dict(self.dic_ai)
								child.last_piece = piece
								child.new_row = new_row
								child.new_col = new_col
								
								if self.state == 'human':
									child.dic_human[piece] = [new_row, new_col]
									child.state = 'ai'

								elif self.state == 'ai':
									child.dic_ai[piece] = [new_row, new_col]
									child.state = 'human'								
									
### gives a board it's score ###	
def analyze_board(dic):
		total = 0
		pawn_weight = 1
		
		# highly experimental
		"""for piece in dic:
			
			if piece[1] == 'P' and dic[piece] != 'dead':
				
				pawn_weight +=1
				
		pawn_weight = (pawn_weight * difficulty)/2
		
		print(pawn_weight)"""
			
		# weights are still undergoing experimentation
		for i in dic:
		
			if dic[i] != 'dead':
			
				if i[1] == 'P':
					total += pawn_weight
					
				elif i[1] == 'K':
					total += 1.5
					
		return total

### checks a list of nodes for highest/lowest score ###		
def best_moves(node_list):

		hi_score = -999
		#low_score = 999 # not used. was used for min
		
		hi_list = []
		#low_list = []
		
		for e in node_list: # loop through all nodes

			cur_score = (analyze_board(e.dic_ai) - analyze_board(e.dic_human)) # ai score - human score
			
			if cur_score > hi_score: # if hiscore beats previous, add it
			
				hi_score = cur_score
			
			#if cur_score < low_score: # if lowscore beats previous, add it
				
				#low_score = cur_score
			
		e = 0 # reset e
		
		for e in range(len(node_list)): # loop thru list again, this time adding best and worst
		
			cur_score = (analyze_board(node_list[e].dic_ai) - analyze_board(node_list[e].dic_human)) # ai score - human score
			
			if cur_score == hi_score: # if cur score equals high score, add it!
			
				hi_list.append(e)
			
			#if cur_score == low_score: # if cur score equals low score, add it!
			
				#low_list.append(e)
				
		return hi_list
									

### now put it all together ###
def get_move(dic_human):
	
	global possible_moves
	global override
	
	# setup a tree and expand it
	top = node()
	top.state = 'original'
	top.dic_ai = state.dic
	top.dic_human = dic_human

	top.grow_tree()
	#print(possible_moves)
	
	
	if override != []: # if there is a move that will lead to a checkmate
		
		best = best_moves(override)
		
		if len(best) > 1:
		
			num = random.randint(0, len(best) - 1) # pick randomly
		
		else:
			
			num = 0
		
		choose = best[num]
		
		chosen_node = override[choose].get_ancestor(3) #get the first move
		
	elif possible_moves != []: # get best moves

		best = best_moves(possible_moves)

		num = random.randint(0, len(best) - 1) # pick randomly
	
		choose = best[num]

		chosen_node = possible_moves[choose].get_ancestor(3) # get the first move
		
	else: # if no moves, game is won/lost or stalemate
		
		return False, False
		
	# if game is won, will throw error, because it can't expand tree
	# these prevent the loss of fun. All about customer service!
	try:
		state.dic[chosen_node.last_piece] = [chosen_node.new_row, chosen_node.new_col] 
	except ValueError:
		return False, False
	except AttributeError:
		return False, False
	
	
	#print(dic_ai[chosen_node.last_piece])
	
	# update ai board
	state.board = grid.recreate_grid(chosen_node.dic_ai)
	#print(override)
	
	# reset moves
	possible_moves = []
	override = []
	
	return state.dic, chosen_node.last_piece

class MSG_Bot:

	def __init__(self):
	
		self.phrases = []
		f = open('resources/msglist.ait', 'r')
		
		for x in range(int(f.readline())):
		
			f.readline()
			
			row = []
			
			for i in range(int(f.readline())):
			
				x = f.readline()
				x = x.rstrip("\n")
				row.append(x)
				
			self.phrases.append(row)

	
	def get_speech(self, phrase_type):
	
		return ('CPU: ' + self.phrases[phrase_type][random.randint(0,len(self.phrases[phrase_type]))-1])

