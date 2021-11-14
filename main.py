import math

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
    res = [2**81] * 9
    for i in range(len(res)):
        for index in boards[i]:
            #can just add instead of using bitwise OR since its not possible for the numbers to overlap
            res[i] += 2**(80 - index)
    return res


def getRow(position):

    row_start = (position // 9) * 9 #returns where the first column of the row will be
    row = 2**(9) - 1 #this creates the binary number 11...1 with 9 ones representing a full row    
    return row<<row_start

def getColumn(position):

    shift = position % 9 #returns the column based on given position aka know how much to shift
    col = 2**0 + 2**9 + 2**18 + 2**27 + 2**36 + 2**45 + 2**54 + 2**63 + 2**72
    #technically I could get a small speed up here by just calculating this number and plugging it in
    #^ this creates a binary number 10...10.. representing a full column

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
            return box
        

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
    #now account for the influence of the current 'queens' for each number
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

def solve(puzzle):
    positions = []
    for i in range(9):
        positions.append(indices(puzzle, i + 1))
    return getAvailableSpots(positions)

def main():

    puzzles, solutions = loadData()
    puzzle = puzzles[0]
    solution = solve(puzzle)
    printPuzzle(puzzle)
    printPuzzle(solutions[0])
    for i in range(len(solution)):
        solution[i] = getPositions(solution[i])
    for row in solution:
        print(row)
if __name__ == "__main__":
    main()
