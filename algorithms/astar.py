from math import sqrt
from math import inf as infinity

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


"""
:return 0 = complete : bpath
        1 = Not done
        -1 = No path
"""


def A_Star(grid, start, goal, d, args=None):
    # ARGS = [openset, closedset, gscore, fscore, cameform]
    h = lambda n: d(n, goal)
    if args is not None:
        open_set = args[0]
        closed_set = args[1]
        gScore = args[2]
        fScore = args[3]
        came_from = args[4]

    # First time
    else:
        open_set = [start]
        closed_set = []

        # came_fron[n] is the parent to n

        came_from = {}

        gScore = {}
        fScore = {}
        # Set default values for all nodes
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                gScore[(i, j)] = infinity
                fScore[(i, j)] = infinity

        gScore[start] = 0
        fScore[start] = h(start)


    if open_set:
        open_set = sorted(open_set, key=lambda cordinate: fScore[cordinate])
        current = open_set[0]
        if current == goal:
            return 0, recunstruct_path(came_from, current), open_set, closed_set

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



        return 1, recunstruct_path(came_from, current), open_set, closed_set, fScore, gScore, came_from

    return -1, None, open_set, closed_set


if __name__ == '__main__':
    m = [[0 for i in range(7)] for j in range(7)]

    start = (6, 0)
    for i in range(1, 5):
        m[i][i] = 3
        
    print_grid(m)
    goal = (0, 6)
    a = A_Star(m, start, goal, distance)

    args = a[2:]

    while a[0] != -1:
        if a[0] == 0:
            finalpath = a[1]
            break

        a = A_Star(m, start, goal, distance, args)
        args = a[2:]
    
    for i,j in finalpath:
        m[i][j] = 1
    print_grid(m)
    print('QUIT')
