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
    #this turns our 'line': represented by 111 into: the box below
    ''' 
    11100000000
    11100000000
    11100000000
    '''
    #taking advantage of dictionary search's speed this is faster than finding starting 
    #row and column for the box and then creating a box instead its just constant 9
    #Nine box dictionaires
    first =   dict({0:0,1:1,2:2, 9:9,10:10,11:11, 18:18,19:19,20:20})
    second =  dict({3:0,4:1,5:2, 12:9,13:10,14:11, 21:18,22:19,23:20})
    third =   dict({6:0,7:1,8:2, 15:9,16:10,17:11, 24:18,25:19,26:20})
    fourth =  dict({27:0,28:1,29:2, 36:9,37:10,38:11, 45:18,46:19,47:20})
    fifth =   dict({30:0,31:1,32:2, 39:9,40:10,41:11, 48:18,49:19,50:20})
    sixth =   dict({33:0,34:1,35:2, 42:9,43:10,44:11, 51:18,52:19,53:20})
    seventh = dict({54:0,55:1,56:2, 63:9,64:10,65:11, 72:18,73:19,74:20})
    eighth =  dict({57:0,58:1,59:2, 66:9,67:10,68:11, 75:18,76:19,77:20})
    ninth =  dict({60:0,61:1,62:2, 69:9,70:10,71:11, 78:18,79:19,80:20})

    if(position in first):
        return box
    if(position in second):
        return box<<3
    if(position in third):
        return box<<6
    if(position in fourth):
        return box<<27
    if(position in fifth):
        return box<<30
    if(position in sixth):
        return box<<33
    if(position in seventh):
        return box<<54
    if(position in eighth):
        return box<<57
    if(position in ninth):
        return box<<60

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
    #note: the idea behind this method is that sudoku is basically
    #n queens problem with 9 queens (except with modified influence since queens cant move in boxes)
    available =  update(available, positions)
    for i in range(start_pos, 81):
        if 2**i & available and 2**i:
            positions += 2**i
            available = update(available, positions)
            #we can skip rest of row if we find a value since we know there CANNOT be another one
            i = i//9 * 9 + 9
    return positions



def main():

    test = [[0]*9 for i in range(9)]
    test[0][4] = 1
    test[3][7] = 1
    test[6][1] = 1

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
