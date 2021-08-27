import random




def create_grid(rows, cols):
    return [[0] * cols for i in range(rows)]


def print_grid(grid):
    for row in grid:
        print(row)


def find_neighbors(grid, i, j):
    neighbors = []
    straight = [(i, j + 2), (i - 2, j), (i + 2, j), (i, j - 2)]

    # Get all neighbors in bounds
    for row, col in straight:
        """1"""
        if 0 <= row < len(grid) and 0 <= col < len(grid[0]) and grid[row][col] != 3:
            neighbors.append((row, col))

    return neighbors


def maze_dfs(grid, start=(0, 0)):
    # Iterative since recursive may generate deep recursion depth
    for i in range(len(grid)):
        if i % 2 == 1:
            for j in range(len(grid[i])):
                grid[i][j] = 3

        else:
            for j in range(1, len(grid[i]), 2):
                grid[i][j] = 3

    # 1. Choose the initial cell, mark it as visited and push it to the stack
    visited = [start]
    stack = [start]
    # 2. While the stack is not empty
    while stack:

        # 2.1 Pop a cell from the stack and make it a current cell
        current = stack[-1]
        stack.pop(-1)
        neighbors = find_neighbors(grid, current[0], current[1])
        random.shuffle(neighbors)
        # 2.2 If the current cell has any neighbours which have not been visited
        if any(n not in visited for n in neighbors):  # checking any elment of list_B in list_A
            # 3.1 Push the current cell to the stack
            stack.append(current)
            # 3.2 Choose one of the unvisited neighbours
            chosen_neighbor = neighbors[0]

            # 3.3 Remove the wall between the current cell and the chosen cell
            w_i, w_j = (int((current[0] + chosen_neighbor[0])/2) , int((current[1] + chosen_neighbor[1])/2))
            grid[w_i][w_j] = 0
            # 3.4 Mark the chosen cell as visited and push it to the stack
            visited.append(chosen_neighbor)
            stack.append(chosen_neighbor)
    return grid


if __name__ == '__main__':
    grid = create_grid(100, 100)
    g = maze_dfs(grid)
    print_grid(grid)
