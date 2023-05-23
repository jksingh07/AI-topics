# Author: Jaskaran Singh Luthra ( 110090236)

# Importing Packages and libraries
from MissionariesCannibals import Missionaries_Cannibals

def main():
    mc_problem = Missionaries_Cannibals()  #calling Missionaries_cannibals function containing solution and methods


    # BFS APPROACH
    print("Using BFS approach\n")
    if(mc_problem.solve(solve_method="dfs")):
        mc_problem.solution()

    else:
        print("Solution Not Found")

    # DFS APPROACH
    print("\n\n\nUsing DFS approach\n")
    if(mc_problem.solve(solve_method="dfs")):
        mc_problem.solution()

    else:
        print("Solution Not Found")



if __name__ == "__main__":
    main()
