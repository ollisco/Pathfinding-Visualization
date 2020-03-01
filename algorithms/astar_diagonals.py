from math import sqrt


def find_neighbors(grid, i, j):
    neighbors = []

    potential_neghbours_straight = [(i, j + 1), (i - 1, j), (i + 1, j), (i, j - 1)]

    # Get all neighbors in bounds
    for a, b in potential_neghbours_straight:
        if 0 <= a < len(grid) and 0 <= b < len(grid[0]):
            neighbors.append((a, b))

    # Topleft
    # 1) Check if diagonal exists
    if (i, j - 1) in neighbors and (i - 1, j) in neighbors:
        # 2) Check if straight negbours are free (not walls)
        if not grid[i][j - 1] == 3 or not grid[i - 1][j] == 3:
            neighbors.append((i - 1, j - 1))

    # Topright
    if (i, j + 1) in neighbors and (i - 1, j) in neighbors:
        if not grid[i][j + 1] == 3 or not grid[i - 1][j] == 3:
            neighbors.append((i - 1, j + 1))

    # Bottomleft
    if (i, j - 1) in neighbors and (i + 1, j) in neighbors:
        if not grid[i][j - 1] == 3 or not grid[i + 1][j] == 3:
            neighbors.append((i + 1, j - 1))

    # Bottomright
    if (i, j + 1) in neighbors and (i + 1, j) in neighbors:
        if not grid[i][j + 1] == 3 or not grid[i + 1][j] == 3:
            neighbors.append((i + 1, j + 1))

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

    else:
        open_set = [start]
        closed_set = []

        # came_fron[n] is the parent to n

        came_from = {}
        gScore = {start: 0}
        fScore = {start: h(start)}

    if open_set:
        open_set = sorted(open_set, key=lambda cordinate: fScore[cordinate])
        current = open_set[0]
        if current == goal:
            return 0, recunstruct_path(came_from, current), open_set, closed_set

        open_set.remove(current)
        closed_set.append(current)

        for neighbor in find_neighbors(grid, *current):
            x, y = neighbor
            if grid[x][y] == 3:
                continue

            if neighbor in closed_set:
                continue

            temp_g = gScore[current] + d(current, neighbor)
            if neighbor not in open_set:
                open_set.append(neighbor)

            elif temp_g >= gScore[neighbor]:
                continue

            came_from[neighbor] = current
            gScore[neighbor] = temp_g
            fScore[neighbor] = gScore[neighbor] + h(neighbor)
        return 1, recunstruct_path(came_from, current), open_set, closed_set, fScore, gScore, came_from

    print('FAIL')
    return -1, None, open_set, closed_set


if __name__ == '__main__':
    m = [[0 for i in range(7)] for j in range(7)]

    start = (0, 0)
    goal = (7, 7)
    a = A_Star(m, start, goal, distance)
    print(a)

    args = a[2:]

    while a[0] != -1:
        if a[0] == 0:
            print('Final path', a[1])
            break

        a = A_Star(m, start, goal, distance, args)
        args = a[2:]

    print('QUIT')
