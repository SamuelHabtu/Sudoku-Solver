import math
import time

def loadData(file_name = "data/data.csv"):
    '''
    function to load the puzzles from text file
    param:
        file_name: defaults to data/data.csv, the name of the data file
    returns:
        puzzles and solutions
    '''
    print(f"loading puzzles from: {file_name[5:]}\n...")
    puzzles = []
    solutions = []
    with open(file_name) as data_file:
        #skip first line since thats where I wrote the format of the data file
        next(data_file)
        for line in data_file:
            puzzle, solution = line.strip().split(',')
            puzzles.append(puzzle)
            solutions.append(solution)
    print("Loading Complete")
    return prepData(puzzles), prepData(solutions)
'''
function has been put away since all it really did was add extra calculations just to
be a minor convenience for me
def reshape(array):
    Function that turns a linear matrix into a square matrix
    param:
        array, the matrix were going to reshape
    returns:
        square matrix
    size = int(len(array)**(1/2))
    matrix = []
    prev = 0
    for i in range(size, size * size + 1, size):
        matrix.append(array[prev: i])
        prev = i
    return matrix
'''
def prepData(sudokus):
    '''
    Function that goes through each index in an array
    param: 
        sudokus, the array containing all the puzzles
    returns:
        result, list of all the sudokus properly done
    '''
    result = []
    for sudoku in sudokus:
        puzzle = [int(value) for value in sudoku]
        result.append(puzzle)
    return result

def bitScan(bitboard):
    #given a bitboard returns the position of the least significant bit
    return bitboard & -bitboard

def getPositions(bitboard):
    '''
    Function that given a bitboard that represents the state of a sudoku returns a list of the positions
    of the bits
    params:
        state: a given bit_board
    returns:
        result: an array of the bit positions
    '''
    result = []
    #since an empty board would be exactly 2**81
    while(bitboard > 2**81):
        sig_bit = bitScan(bitboard)
        result.append(int(math.log(sig_bit, 2)))
        bitboard -= sig_bit    
    return result

def getBitboards(boards):
    '''
    Function returns 9 bitboards representing the positions of each digit from a sudoku puzzle
    '''
    #start off each bitboard with 2^81 which is a binary number that consists of
    #81 zeroes and 1 leading 1
    positions = [2**81] * 9
    for i in range(len(positions)):
        for index in boards[i]:
            #can just add instead of using bitwise OR since its not possible for the numbers to overlap
            positions[i] += 2**(80 - index)
    return positions


def getRow(position):

    row_start = (position // 9) * 9 #returns where the first column of the row will be
    row = 2**(9) - 1 #this creates the binary number 11...1 with 9 ones representing a full row    
    return row<<row_start

def getColumn(position):

    shift = position % 9 #returns the column based on given position aka know how much to shift
    col = 0x1008040201008040201
    #this hex constant is just 2**0 + 2**9 + 2**18 + 2**27 + 2**36 + 2**45 + 2**54 + 2**63 + 2**72
    #which is the first column, then based on which column our position belongs to
    #we shift our column to the appropiate column
    return col<<shift  

def getBox(position):
    line = 7
    box = line| line<<9 | line<<18
    #this turns our 'line': represented by 111 into: the 'box' below
    ''' 
    00000000111
    00000000111
    00000000111
    '''
    position = 2**position
    #decided to just write out the shifts for the sake of simplicity
    for shift in (0,3,6,27,30,33,54,57,60):
        if(position & box<<shift):
            return box<<shift
        
def influence(position):
    #given the position of a number on a sudoku board, returns it's influence in th form of a bitboard
    return (getRow(position) | getColumn(position) | getBox(position)) | 2**81

def update(available, positions):
    return available & ~influence(positions)

def indices(arr, target):
    #given a target number this function returns a list of the indices of instances of that number
    #within a given array
    return [(80 - i) for i, value in enumerate(arr) if value == target]

def emptySpots(arr):
    return [(80 - i) for i, value in enumerate(arr) if not value]

def printPuzzle(puzzle):
    for i in range(0, 81, 9):
        print(puzzle[i:i+9])
    print()

def getAvailableSpots(positions):
    '''
    Function figures out the available spots
    on a sudoku puzzle for each number
    params:
        puzzle: a sudoku puzzle in the form of a 81 length list
    returns:
        available: an array that contains the bitboards for available positions
    '''
    boards = []
    influenced = [0]*9
    available = [0]*9
    boards = getBitboards(positions)
    #first account for positions that are already filled since we cant just overwrite our puzzle
    filled_spots = 0
    for i in range(len(positions)):
        for position in positions[i]:
            filled_spots += 2**position
    #note: the idea behind this method is that sudoku is how I personally try to solve sudoku puzzles
    #I look at what spots are 'covered' by a number, sort of like the n-queens problem
    #except theres 9 different queens that influence a different shape(square, row and col)
    for i in range(len(boards)):
        for position in positions[i]:
            influenced[i] = influenced[i] | influence(position)
        available[i] = (filled_spots | influenced[i]) ^ ((2**81) - 1)
    #remove the positions we already know are filled
    #in order to be available a position has to be not influenced
    return available

def getOptions(available, empty):
    
    options = dict({})
    #convert the bitboards into lists for convenience
    for position in empty:
        #for every new positions we must first put in an empty list for all of its possible digits
        if(position not in options):
            options[position] = []
        for i in range(len(available)):
            if(2**position & available[i]):
                options[position].append(i + 1)
    return options 
    
def simplify(options, available):
    filled = dict({})
    #function that goes through the options and for each spot where there is only 1 choice it does it
    prev = options.copy()
    while(options):
        for spot in options:
            if(len(options[spot]) == 1):
                filled[spot] = options[spot][0]
        #delete every spot we've filled
        for spot in filled:
            if(spot in options):
                del options[spot]
        #if we did not change options at all then we've either solved the puzzle or gotten stuck
        if(options == prev):
            options = 0
        #update options by finding out what is now available
        for spot in filled:
            available[filled[spot] - 1] = available[filled[spot] - 1] & ~influence(spot)
        if(options):
            options = getOptions(available, options.keys())
            #update prev
            prev = options.copy()
    return filled
        
def solve(puzzle):
    positions = []
    for i in range(9):
        positions.append(indices(puzzle, i + 1))
    available = getAvailableSpots(positions)
    empty = emptySpots(puzzle)
    #options will become a dictionary with the empty spots as keys and 
    #all the digits with that as an available value
    options = getOptions(available, empty)
    simplified = simplify(options, available)
    for position in simplified:
        puzzle[80 - position] = simplified[position]
    return puzzle

def main():
    print("Welcome to sudoku solver")
    choice = input("Enter 1 for the sample cases or 2 to enter your own puzzle:")
    if(choice == "2"):
        print("starting from the top-left and going right enter each digit seperated by spaces")
        print("e.g: 3 0 7 0 1 0 0 2 0 4 0 5 0 0 3 0 0 0 0 8 2 5 0 9 0 4 3 0 0 0 0 7 8 1 0 0 0 0 1 2 0 6 5 0 0 7 2 9 4 0 0 0 0 0 0 0 0 0 8 2 0 3 1 0 4 0 0 3 0 9 6 7 0 0 3 6 0 0 0 0 0")
        user_input = input(f"Enter your Puzzle: ")
        #using list comprehension to quickly convert the goods :O
        puzzle = [int(value) for value in user_input.split()]
        print("")
        printPuzzle(puzzle)
        start_time = time.perf_counter()
        solution = solve(puzzle.copy())
        end_time = time.perf_counter()
        printPuzzle(solution)
        print(f"it took {round( (end_time - start_time) * 1000)} ms")
        if(0 in solution):
            print("Could not completely solve this puzzle, did as many logical moves as possible")
        
    if(choice == "1"):
        test()
def test():
    #if user does not want provide input we test every single puzzle we have in data.csv
    puzzles, solutions = loadData()
    times = []
    for i in range(len(puzzles)):
        puzzle = puzzles[i].copy()
        start_time = time.perf_counter()
        solution = solve(puzzle.copy())
        end_time   = time.perf_counter()
        times.append(round( (end_time - start_time) * 1000))
        printPuzzle(puzzle)
        printPuzzle(solution)
        print(f"it took {times[i]} ms to solve this puzzle")
        print(["Solution is incorrect","Solution is correct"][solution == solutions[i]])
    print(f"average time to complete each puzzle: {sum(times)/len(times)} ms")

if __name__ == "__main__":
    main()
    
