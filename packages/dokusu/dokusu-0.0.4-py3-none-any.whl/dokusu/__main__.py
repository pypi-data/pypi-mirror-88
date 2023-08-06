from core import *
from rules import *

def main():
    
    sudoku = Sudoku.sample()
    # sudoku = Sudoku.from_numpy(<np array here>)

    solved = sudoku.solve()

    print(solved) # np array (9, 9)
    pass


if __name__ == "__main__":
    main()
