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

def CalcErrors(sudoku):
    print("\n")
    errors = 0
    tempCol = [0] * 9
    tempRow = [0] * 9

    for i in range (0,9):
        tempCol[i] = sudoku[i,0]
        for j in range(0,9):
            tempRow[j] = sudoku[i,j]
        errors += CheckRow(tempRow)
    return(errors)

def CheckRow(row):
    errors = 0
    for i in range (0,9):
       for j in range (0,9):
           if j == row[i]:
               errors += 1
    print(errors)
    return(errors)

PrintSudoku(sudoku)
CalcErrors(sudoku)
