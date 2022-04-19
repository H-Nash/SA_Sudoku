import pulp as plp

class Linear:
    def __init__(self, game):
        self.input_game = game
        self.solution = list()

        self.problem = plp.LpProblem("Sudoku Game")
        self.rows, self.cols, self.grids, self.values = [range(9), range(9), range(9), range(1,10)]
        self.grid_v = plp.LpVariable.dicts("grid_v",(self.rows,self.cols,self.values),cat="Binary")

        self.objective = plp.lpSum(0)
        self.problem.setObjective(self.objective)

        self.set_constraints(game.getBoard(), self.problem, self.grid_v, self.rows, self.cols, self.grids, self.values)
        self.add_prefilled_constraints(self.problem, game.getBoard(), self.grid_v, self.rows, self.cols, self.values)
        pass

    def solve(self):
        self.problem.solve()
        status = plp.LpStatus[self.problem.status]
        print(f'Solution Status = {plp.LpStatus[self.problem.status]}')

        if status == "Optimal":
            self.solution = self.collect(self.grid_v, self.rows, self.cols, self.values)

    def apply_solution(self):
        self.input_game.apply_solution(self.solution)
    
    def add_prefilled_constraints(self, prob, input_sudoku, grid_vars, rows, cols, values):
        for row in rows:
            for col in cols:
                if(input_sudoku[row][col] != 0):
                    prob.addConstraint(plp.LpConstraint(e=plp.lpSum([grid_vars[row][col][value]*value  for value in values]), 
                                                        sense=plp.LpConstraintEQ, 
                                                        rhs=input_sudoku[row][col],
                                                        name=f"constraint_prefilled_{row}_{col}"))

    def set_constraints(self, game, prob, grid_vars, rows, cols, grids, values):
        for row in rows:
            for col in cols:
                    prob.addConstraint(plp.LpConstraint(e=plp.lpSum([grid_vars[row][col][value] for value in values]),
                                            sense=plp.LpConstraintEQ, rhs=1, name=f"constraint_sum_{row}_{col}"))    
        for row in rows:
            for value in values:
                prob.addConstraint(plp.LpConstraint(e=plp.lpSum([grid_vars[row][col][value]*value  for col in cols]),
                                            sense=plp.LpConstraintEQ, rhs=value, name=f"constraint_uniq_row_{row}_{value}"))      
        for col in cols:
            for value in values:
                prob.addConstraint(plp.LpConstraint(e=plp.lpSum([grid_vars[row][col][value]*value  for row in rows]),
                                            sense=plp.LpConstraintEQ, rhs=value, name=f"constraint_uniq_col_{col}_{value}"))     
        for grid in grids:
            grid_row  = int(grid/3)
            grid_col  = int(grid%3)

            for value in values:
                prob.addConstraint(plp.LpConstraint(e=plp.lpSum([grid_vars[grid_row*3+row][grid_col*3+col][value]*value  for col in range(0,3) for row in range(0,3)]),
                                            sense=plp.LpConstraintEQ, rhs=value, name=f"constraint_uniq_grid_{grid}_{value}"))
    
    def collect(self, grid, rows, cols, values):
        sol = [[0 for c in cols] for r in rows]
        for r in rows:
            for c in cols:
                for v in values:
                    if plp.value(grid[r][c][v]):
                        sol[r][c] = v
        return sol
                        