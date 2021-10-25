from sudoku import Sudoku

def loadData(file_name = "data/data.csv"):
    '''
    function to load the puzzles from text file
    param:
        file_name: defaults to data/data.csv, the name of the data file
    returns:
        puzzles and solutions
    '''
    print(f"loading {file_name[5:-4]}")
    puzzles = []
    solutions = []
    with open(file_name) as data_file:
        #skip first line since thats where I wrote the format of the data file
        next(data_file)
        for line in data_file:
            puzzle, solution = line.strip().split(',')
            puzzles.append(puzzle)
            solutions.append(solution)
    return prepData(puzzles), prepData(solutions)

def reshape(array):
    '''
    Function that turns a linear matrix into a square matrix
    param:
        array, the matrix were going to reshape
    returns:
        square matrix
    '''
    size = int(len(array)**(1/2))
    matrix = []
    prev = 0
    for i in range(size, size * size + 1, size):
        matrix.append(array[prev: i])
        prev = i
    return matrix

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
        result.append(reshape(puzzle))
    return result

def interpret(state, value):
    '''
    Function that given a bitboard that represents the state of a sudoku returns a list version of it
    params:
        state: a given bit_board
        value: the value were placing in each valid location on that bitboard
    returns:
        an nxn list containing the information from the bitboard
    '''
    result = [0] * 81
    for j in range(len(result)):
        if 2**j & state:
            result[j] = value
    return reshape(result)

def getRow(position):

    row_start = (position // 9) * 9
    board = 2**row_start
    return board | board<<1 | board<<2 | board<<3 | board<<4 | board<<5 | board<<6 | board<<7 | board<<8  

def getColumn(position):

    col_start = position % 9
    board = 2**col_start
    return board | board<<9 | board<<18 | board<<27 | board<<36 | board<<45 | board<<54 | board<<63 | board<<72 

def getBox(position):

    if position > 63 and position < 72:
        position -= 9
    if position >= 72:
        position -= 18
    box_start = (position//3 * 3 )
    board = 2**box_start
    box_row = board | board<<1 | board<<2
    return (box_row | box_row<<9 | box_row<<18)

def influence(positions):

    row = 0
    column = 0
    box = 0
    print(f"positions: {positions}")
    for i in range(81):
        if 2**i & positions:
            column    += getColumn(i)
            row       += getRow(i)
            box       += getBox(i)
    return (row | column | box) | 2**81

def update(available, positions):
    return available & ~influence(positions)

def solve(boards, index, start_pos = 0):
    '''
    Function that returns an NQueens style problem using bitboards for a gaven number
    params:
        boards: a list containing 9 bitboards that represent the positions of each number
        index: the index that contains our target number
    returns: solved_bitboard

    '''
    #2^(n^2) - 1 :where n is the number of rows, this bitboard would look like 1111...1
    available = 2**(len(boards)**2) - 1 
    positions = boards[index]
    #remove the positions we already know are filled
    for board in boards:
        available = available & ~board
    #account for the influence of the current 'queens'
    available =  update(available, positions)
    for i in range(start_pos, 81):
        if 2**i & available and 2**i:
            positions += 2**i
            available = update(available, positions)
            i = i//9 * 9 + 9
    return positions



def main():

    test = [[0]*9 for i in range(9)]
    test[0][0] = 1
    test[3][3] = 1
    test[6][6] = 1

    sudoku = Sudoku()
    sudoku.readPuzzle(test)
    sudoku.printPuzzle()
    inf = influence(sudoku.state[0])
    print("influence ",inf)
    

def test():

    sudoku = Sudoku()
    puzzles, solutions = loadData()
    sudoku.readPuzzle(puzzles[3])
    result = [[0]*9]*9

    for i in range(1):
        sol = solve(sudoku.state, i)
        for row in interpret(sol, i + 1):
            for j in range(len(row)):
                if(row[j]):
                    result[i][j] = row[j]

    print("Puzzle:")
    sudoku.printPuzzle()

    print("Algo Result")
    for row in result:
        print(row)
    
    print("Real Solution")
    sudoku.readPuzzle(solutions[3])
    sudoku.printPuzzle()

if __name__ == "__main__":
    main()
