"""
NAME
pacman - Takes an input text file with given board dimension, initial position, walls and directions for a game of pacman. 
Returns final x and y coordniates of pacman's position along with the coins collected.

FUNCTIONS
    pacman
        FUNCTIONS
            unexpectedCharacters
                No input parameters passed. Returns boolean indicating if unexpected characters found in input file
            unexpectedDimensions
                No input parameters passed. Returns boolean indicating if dimensions given in input file were unexpected
            unexpectedInitialPos
                No input parameters passed. Returns boolean indicating if initial position given in input file was unexpected
            unexpectedDirections
                No input parameters passed. Returns boolean indicating if directions given in input file were unexpected
            unexpectedWalls
                No input parameters passed. Returns boolean indicating if walls given in input file were unexpected
            createBoard
                No input parameters passed. Returns 2D array representing the pacman game board 
            traverseBoard
                No input parameters passed. Returns final positions in x,y coordinates and coins collected after traversal of board
"""

__author__ = "Hardik Sangwan"

import re

def pacman(input_file):
    '''
    Solution setup:
    1. Get File Contents
    2. Check for Edge Cases
    3. Create Board
    4. Traverse Board
    5. Return Final Position and Coin Count
    '''

    #Helper Functions -> Edge Cases, Board Setup, Board Traversal

    def unexpectedCharacters():
        '''
        File should only contain numbers 0-9 for coordinates, N S E W for directions and whitespace. 
        Quick prelim check before going further.
        returns true if unexpected characters found, false otherwise.
        '''
        file = open(input_file)
        components = file.read()
        file.close()
        pattern = re.compile('[^0-9NSWE\s]')
        if pattern.search(components) == None:
            return False
        else:
            return True

    def unexpectedDimension():
        '''
        Checking 1st line for board dimensions.
        Possible issues: 0 for either dimension. More/Less than 2 numbers on 1st line. Direction alphabets on 1st line
        returns true if any issues found, false otherwise.
        '''
        boardDimensions = components[0].rstrip().split()
        pattern = re.compile('[^0-9\s]')
        if len(boardDimensions) != 2 or boardDimensions[0] == '0' or boardDimensions[1] == '0' or pattern.search(components[0]) != None:
            return True
        else:
            return False

    def unexpectedInitialPos():
        '''
        Checking 2nd for initial position.
        Possible issues: Position exceeding dimensions. More/Less than 2 numbers on 2nd line. Direction alphabets on 2nd line
        returns true if any issues found, false otherwise.
        '''
        InitialPos = components[1].rstrip().split()

        #Alphabet Check separate to avoid string exception thrown by converting to int()
        pattern = re.compile('[^0-9\s]')
        if pattern.search(components[1]) != None:
            return True

        if len(InitialPos) != 2 or int(InitialPos[0]) >= int(components[0].rstrip().split()[0])\
         or int(InitialPos[1]) >= int(components[0].rstrip().split()[1]):
            return True
        else:
            return False

    def unexpectedDirections():
        '''
        Checking 3rd line for directions.
        Possible issues: numbers for directions
        returns true if any issues found, false otherwise.
        '''
        pattern = re.compile('[^NSWE\s]')
        if pattern.search(components[2]) != None:
            return True
        else:
            return False

    def unexpectedWalls():
        '''
        Checking 4th line till end of file for walls.
        Possible issues: More/Less than 2 numbers on a line. Direction alphabets on a line
        returns true if any issues found, false otherwise.
        '''
        walls = components[3:]
        pattern = re.compile('[^0-9\s]')
        i = 3
        for wall in walls:
            if len(wall.rstrip().split()) != 2 or pattern.search(components[i]) != None:
                return True
            i += 1
        return False

    def createBoard(): 
        #Returns 2D array with board dimensions; 1s at all coordinates without walls. x's at all coordinates with walls
        col = int(components[0].rstrip().split()[0])
        row = int(components[0].rstrip().split()[1])
        board = [[1 for x in range(col)] for y in range(row)]
        walls = components[3:]
        for wall in walls:
            wall = wall.rstrip().split()
            if int(wall[0]) < row and int(wall[1]) < col:
                board[int(wall[0])][int(wall[1])] = 'x'
        return board
    
    def traverseBoard(): 
        '''
        set coin at initial position on board to zero.
        move pacman and keep track of current position and coins collected. 
        Remove coins from previously visited locations. Shouldn't double count already eaten coins
        keep moving until last direction.
        return final x pos, final y pos and coins collected
        '''
        InitialPos = components[1].rstrip().split()
        final_pos_x = int(InitialPos[0])
        final_pos_y = int(InitialPos[1])
        board[final_pos_x][final_pos_y] = 0
        coins_collected = 0

        directions = list(components[2].rstrip())
        for direction in directions:
            if direction == 'N':
                if final_pos_y + 1 < len(board[0]) and board[final_pos_x][final_pos_y + 1] != 'x':
                    final_pos_y += 1
                    if board[final_pos_x][final_pos_y] > 0:
                        coins_collected += board[final_pos_x][final_pos_y]
                        board[final_pos_x][final_pos_y] -= 1

            if direction == 'S':
                if final_pos_y - 1 >= 0 and board[final_pos_x][final_pos_y - 1] != 'x':
                    final_pos_y -= 1
                    if board[final_pos_x][final_pos_y] > 0:
                        coins_collected += board[final_pos_x][final_pos_y]
                        board[final_pos_x][final_pos_y] -= 1

            if direction == 'E':
                if final_pos_x + 1 < len(board) and board[final_pos_x + 1][final_pos_y] != 'x':
                    final_pos_x += 1
                    if board[final_pos_x][final_pos_y] > 0:
                        coins_collected += board[final_pos_x][final_pos_y]
                        board[final_pos_x][final_pos_y] -= 1

            if direction == 'W':
                if final_pos_x - 1 >= 0 and board[final_pos_x - 1][final_pos_y] != 'x':
                    final_pos_x -= 1
                    if board[final_pos_x][final_pos_y] > 0:
                        coins_collected += board[final_pos_x][final_pos_y]
                        board[final_pos_x][final_pos_y] -= 1

        return final_pos_x, final_pos_y, coins_collected
    
    #1. Get File Contents
    try:
        with open(input_file, 'r') as file:
            components = file.readlines()
            file.close()
    except Exception:
        return (-1, -1, 0)

    #2. Check for Edge Cases
    if unexpectedCharacters() or unexpectedDimension() or unexpectedDirections() or unexpectedInitialPos() or unexpectedWalls():
        print (-1, -1, 0)
        return (-1, -1, 0) #Arbitrary return values decided for edge cases

    #3. Create Board

    board = createBoard()

    final_pos_x, final_pos_y, coins_collected = traverseBoard()

    print(final_pos_x, final_pos_y, coins_collected)
    return (final_pos_x, final_pos_y, coins_collected) 
