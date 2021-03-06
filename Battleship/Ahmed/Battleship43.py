#********************************************
# By Ahmed Elbannan
# September 22nd 2013
# Battleship CPSC231 (Limited Edition! ;] )
#********************************************

# CONSTANTS values 
GRID_HEIGHT = 10;
GRID_WIDTH = 10;
VESSEL_NAME = ['Aircraft Carrier', 'Battleship', 'Submarine', 'Destroyer', 'Patrol Boat'];
VESSEL_SIZE = [5, 4, 3, 2, 2];
NAME = '';

# global variables
direction = 'horizontal';
x = ord('A');
y = 0;

w = '~'
grid = 		[
			[w,w,w,w,w,w,w,w,w,w],
			[w,w,w,w,w,w,w,w,w,w],
			[w,w,w,w,w,w,w,w,w,w],
			[w,w,w,w,w,w,w,w,w,w],
			[w,w,w,w,w,w,w,w,w,w],
			[w,w,w,w,w,w,w,w,w,w],
			[w,w,w,w,w,w,w,w,w,w],
			[w,w,w,w,w,w,w,w,w,w],
			[w,w,w,w,w,w,w,w,w,w],
			[w,w,w,w,w,w,w,w,w,w],
			[w,w,w,w,w,w,w,w,w,w]];

# Title Screen! Now a function!
def print_titlescreen():
	
	global NAME;
	print();
	print('________________________________________');
	print('|*********WELCOME TO BATTLESHIP!*******|');
	print('|**************************************|');
	print('|**************************************|');
	print('|*********A game like no other!********|');
	print('|**************************************|');
	print('|**************************************|');
	print('|**************************************|');
	print();
	NAME = 'Admiral ' + input('What is your name? ');
	print();
# end
			
# print out the grid			
def print_grid():
	
	print('__________________________');
	print('|  | A B C D E F G H I J |');
	print('--------------------------');
	row = 0;
	column = 0;
	
	# print the grid using a nested for loop
	for row in range(GRID_HEIGHT):
		
		if row  == 9:
			print( '|' + str(row + 1) + '| ', end = '');
		else:
			print( '|0' + str(row + 1) + '| ', end = '');			
		for column in range(0, GRID_WIDTH):
			print(grid[column][row] + ' ', end = '');
		print('|');
		
	print();

# let's the user choose where to place vessel
def get_location(index):
	
	global x; # this function can edit x
	global y; # this function can edit y
	global direction; # this function can edit direction
	# Get row, column, direction from player
	print (NAME + ', where would you like to place your ' + VESSEL_NAME[index] + '? (' + str(VESSEL_SIZE[index]) + ' spaces)');
	x = input('Horizontal position, Sir?(A-J):');
	y = input('Vertical position? (1-10):');
	direction = input('Direction? [h]orizontal or [v]ertical:');
	print();
# end

# put vessel on board
def place_vessel(index):
	
	global x;
	global y;
	
	#check if direction is h or v, then places ship accordingly
	if direction == 'h': 
			for x in range(x, x + VESSEL_SIZE[index]):
				grid[x][y] = str(VESSEL_SIZE[index]);
				
	elif direction == 'v':
			for y in range(y, y + VESSEL_SIZE[index]):
				grid[x][y] = str(VESSEL_SIZE[index]);
				
# checks if the location is valid
def validate_location(index):
	
	global x; # this function can edit x
	global y; # this function can edit y
	# check if string is a single letter or smaller than a three digit number, if not, asks for input again, then checks
	
	#check if strings are appropriate length
	if (len(x) == 1) and (len(y) < 3):
		x = (ord(x) - ord('A'));
		y = (int(y) - 1);
		
		# checks if location is on the board and if the ship will fit, if not asks for input again and checks again
		if (direction == 'h') and (-1 < x < (GRID_WIDTH - VESSEL_SIZE[index])) and (-1 < y < GRID_HEIGHT):
			place_vessel(index);
			
		elif direction == 'v' and (-1 < y < (GRID_HEIGHT - VESSEL_SIZE[index])) and (-1 < x < GRID_WIDTH):  
			place_vessel(index);
			
		else:
			print('The location you entered is not on the board!');
			get_location(index);
			validate_location(index); # recursive
			
	else:
		print('Please enter a LETTER (between A-J) and a NUMBER (between 1-10!)');
		get_location(index);
		validate_location(index); # recursive
	return;
	
# doesn't quit unless q is entered	
def enter_choice():
	choice = '';
	while not choice == 'q':
		choice = input('Enter choice: ');
		
# now put it all together!
def main():
        
        # prints VESSEL_NAME[index], location, and orientation of a vessel
	print_titlescreen();
	print_grid();
        # Ask user to place all 5 ships
	i = 0;
	for i in range(5): # for loop
		get_location(i);
		validate_location(i);
		print_grid();
	
	enter_choice();
	return;
# end

main(); 
