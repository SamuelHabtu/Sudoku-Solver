class Sudoku(object):

    def __init__(self):
        #will represent 9 81-bit arrays for each number
        self.state = [0] * 9 
        self.puzzle = [[0] * 9] * 9

    def readPuzzle(self, puzzle):

        if len(puzzle) != 9 and len(puzzle[0]) != 9:
            raise Exception(f"invalid puzzle size: Must be 9x9 but it is {len(puzzle)}x{len(puzzle[0])}")
        self.puzzle = puzzle
        for i in range(len(puzzle)):
            for j in range(len(puzzle[0])):
                if puzzle[i][j]:
                    value = puzzle[i][j]
                    self.state[value - 1] += 2**(80 - (i * 9 + j))

    def printPuzzle(self):
    	
        for row in self.puzzle:
            print(row)
        print()

    def update(self, state):

        self.state = state
        for i in range(1, 10):
            state = self.state[i - 1]
            for j in range(9):
                for k in range(9):
                    if 2**(j*9 + k) & state:
                        self.puzzle[j][k] = i



                