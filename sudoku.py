class Sudoku(object):

    def __init__(self, puzzle = [[0] * 9] * 9):
        self.puzzle = puzzle

    def update(self, puzzle):
        self.puzzle = puzzle

    def readPuzzle(self, puzzle):

        if len(puzzle) != 81:
            raise Exception(f"invalid puzzle size: Must have 81 Spaces but it is {len(puzzle)} spaces")
        self.puzzle = puzzle
    def printPuzzle(self):

        for i in range(0, 81, 9):
            print(self.puzzle[i:i+9])
        print()


                