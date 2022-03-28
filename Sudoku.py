import numpy as np

initSudoku = """
                703100904
                405000073
                020304105
                670030089
                031640050
                000020010
                000400208
                006208500
                004750690                    
                """

sudoku = np.array([[int(i) for i in line] for line in initSudoku.split()])

def PrintSudoku(sudoku):
    print("\n")
    
    for i in range(len(sudoku)):
        line = ""

        if i == 3 or i == 6:
            print("---------------------")

        for j in range(len(sudoku[i])):

            if j == 3 or j == 6:
                line += "| "
            line += str(sudoku[i,j])+" "

        print(line)

PrintSudoku(sudoku)
