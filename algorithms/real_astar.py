from math import sqrt, inf


def create_grid(rows, cols):
    return [[0] * cols for i in range(rows)]


def print_grid(grid):
    for row in grid:
        print(row)


def find_neighbors(grid, i, j):
    neighbors = []
    # diagonal = [(i - 1, j - 1), (i + 1, j - 1), (i - 1, j + 1), (i + 1, j + 1)]
    straight = [(i, j + 1), (i - 1, j), (i + 1, j), (i, j - 1)]

    # Get all neighbors in bounds
    for row, col in straight:
        if 0 <= row < len(grid) and 0 <= col < len(grid[0]) and grid[row][col] != 3:
            neighbors.append((row, col))

    return neighbors


def distance(n, goal):
    d = sqrt((goal[0] - n[0]) ** 2 + (goal[1] - n[1]) ** 2)
    return d


def recunstruct_path(came_from, current):
    last_node = current
    total_path = []
    while current in list(came_from.keys()):
        total_path.append(current)
        current = came_from[current]
    # Adds the stating node
    return total_path


def astar(grid, start, goal, d):
    h = lambda n: d(n, goal)

    steps = []

    open_set = [start]
    closed_set = []

    # came_fron[n] is the parent to n

    came_from = {}

    gScore = {}
    fScore = {}
    # Set default values for all nodes
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            gScore[(i, j)] = inf
            fScore[(i, j)] = inf

    gScore[start] = 0
    fScore[start] = h(start)

    while open_set:

        open_set = sorted(open_set, key=lambda cordinate: fScore[cordinate])
        current = open_set[0]
        if current == goal:
            return steps

        open_set.remove(current)
        closed_set.append(current)

        for neighbor in find_neighbors(grid, *current):

            temp_g = gScore[current] + d(current, neighbor)
            if temp_g < gScore[neighbor]:

                came_from[neighbor] = current
                gScore[neighbor] = temp_g
                fScore[neighbor] = gScore[neighbor] + h(neighbor)
                if neighbor not in open_set:
                    open_set.append(neighbor)

        this_grid = grid
        for i, j in closed_set:
            this_grid[i][j] = 4

        for i, j in open_set:
            this_grid[i][j] = 5

        for i, j in recunstruct_path(came_from, current):
            this_grid[i][j] = 2

        this_grid[start[0]][start[1]] = 6
        this_grid[goal[0]][goal[1]] = 7



        steps.append(this_grid)

    return -1


if __name__ == '__main__':
    grid = create_grid(5, 5)
    start = (0, 0)
    goal = (4, 4)
    print_grid(grid)
    print()
    steps = astar(grid, start, goal, distance)
    print("----------------------------------------")
    for step in steps:
        print_grid(step)
        print()
