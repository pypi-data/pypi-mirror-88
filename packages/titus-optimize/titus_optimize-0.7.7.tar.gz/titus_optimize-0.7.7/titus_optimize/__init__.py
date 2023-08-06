import cvxpy as cp

def fast_solve(problem, solver, verbose, **kwargs):
    '''
    This function exists to bypass some of the expensive
    checks and heuristics cvxpy usually use to select a 
    solver or make sure the problem is DCP.
    '''
    from cvxpy.problems.objective import Maximize
    from cvxpy.reductions import (
                              FlipObjective, Qp2SymbolicQp,
                              CvxAttr2Constr,
                              EvalParams,
                              QpMatrixStuffing)
    from cvxpy.reductions.solvers import defines as slv_def

    solver_instance = slv_def.SOLVER_MAP_QP[cp.settings.GUROBI]

    reductions = []
    if type(problem.objective) == Maximize:
        reductions += [FlipObjective()]
    reductions += [CvxAttr2Constr(), Qp2SymbolicQp()]
    
    reductions += [EvalParams()]
    reductions += [QpMatrixStuffing(),
                    solver_instance]

    solving_chain = cp.reductions.solvers.solving_chain.SolvingChain(
        reductions=reductions)

    data, inverse_data = solving_chain.apply(problem)

    solution = solving_chain.solve_via_data(
        problem, data,
        False, # warm_start
        verbose, kwargs)
    problem.unpack_results(solution, solving_chain, inverse_data)
    return problem.value

cp.Problem.register_solve("fast", fast_solve)