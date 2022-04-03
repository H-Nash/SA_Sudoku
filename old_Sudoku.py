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

    #Row Errors
    print ("\nRow Error Checking In Progress")
    print ("------------------------------")
    for i in range (0,9):
        line = ""
        for j in range(0,9):
            tempRow[j] = sudoku[i,j]
            line += str(tempRow[j]) + " "
        print(line)
        errors += CheckRow(tempRow)

    #Column Errors
    print ("\nColumn Error Checking In Progress")
    print ("---------------------------------")
    for i in range (0,9):
        line = ""
        for j in range (0,9):
            tempCol[j] = sudoku[j,i]
            line += str(tempCol[j]) + " "
        print(line)
        errors += CheckCol(tempCol)

    return(errors)

def CheckRow(row):
    errors = len(row) - len(np.unique(row))
    print(errors)
    return(errors)

def CheckCol(col):
    errors = len(col) - len(np.unique(col))
    print(errors)
    return(errors)

PrintSudoku(sudoku)
CalcErrors(sudoku)
