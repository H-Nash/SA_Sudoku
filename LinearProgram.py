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
        pass

    def solve(self):
        self.problem.solve()

        status = plp.LpStatus[self.problem.status]
        print(f'Solution Status = {plp.LpStatus[self.problem.status]}')

        #if status == "Optimal":
        self.solution = self.collect(self.grid_v, self.rows, self.cols, self.values)

    def apply_solution(self):
        self.input_game.apply_solution(self.solution)

    def set_constraints(self, game, prob, grid, rows, cols, grids, values):
        #One value in cell
        for r in rows:
            for c in cols:
                prob.addConstraint(plp.LpConstraint(e=plp.lpSum([grid[r][c][v] for v in values]),
                    sense=plp.LpConstraintEQ, rhs=1, name=f"constraint_sum_{r}_{c}"))


        # Row only 1-9       
        for r in rows:
            for v in values:
                prob.addConstraint(plp.LpConstraint(e=plp.lpSum([grid[r][c][v]*v for c in cols]),
                    sense=plp.LpConstraintEQ, rhs=v, name=f"constraint_uniq_row_{r}_{v}"))

        # Col only 1-9     
        for c in cols:
            for v in values:
                prob.addConstraint(plp.LpConstraint(e=plp.lpSum([grid[r][c][v]*v  for r in rows]),
                    sense=plp.LpConstraintEQ, rhs=v, name=f"constraint_uniq_col_{c}_{v}"))


        # Fill 3x3 Block once  
        for g in grids:
            g_r  = int(g/3) #row
            g_c  = int(g%3) #col

            for v in values:
                prob.addConstraint(plp.LpConstraint(e=plp.lpSum([grid[g_r*3+r][g_c*3+c][v]*v  for c in range(0,3) for r in range(0,3)]),
                    sense=plp.LpConstraintEQ, rhs=v, name=f"constraint_uniq_grid_{g}_{v}"))
        
        for r in rows:
            for c in cols:
                if(game[r][c] != 0):
                    prob.addConstraint(plp.LpConstraint(e=plp.lpSum([grid[r][c][v]*v for v in values]),
                        sense=plp.LpConstraintEQ, rhs = game[r][c], name=f"constraint_prefilled_{r}_{c}"))
    
    def collect(self, grid, rows, cols, values):
        sol = [[0 for c in cols] for r in rows]
        for r in rows:
            for c in cols:
                for v in values:
                    if plp.value(grid[r][c][v]):
                        sol[r][c] = v
        return sol
                    