from math import sqrt
from math import inf as infinity


def print_grid(grid):
    for row in grid:
        print(row)




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


#
def dijkstra(grid, start, goal, d, args=None):
    # args = [unvisited_nodes, distance_from_start, came_from, visited]

    # If run before
    if args is not None:

        unvisited_nodes = args[0]
        distance_from_start = args[1]
        came_from = args[2]
        visited_nodes = args[3]
    # First time
    else:
        unvisited_nodes = []
        visited_nodes = []
        distance_from_start = {}
        came_from = {}
        current = start

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                distance_from_start[(i, j)] = infinity

                unvisited_nodes.append((i, j))
        distance_from_start[start] = 0

    if unvisited_nodes:

        unvisited_nodes = sorted(unvisited_nodes, key=lambda cordinate: distance_from_start[cordinate])
        current = unvisited_nodes[0]

        # No solution
        if distance_from_start[current] == infinity:
            return -1, None, [unvisited_nodes, distance_from_start, came_from, visited_nodes]
        unvisited_nodes.remove(current)
        visited_nodes.append(current)

        if goal in visited_nodes:
            return 0, recunstruct_path(came_from, goal), [unvisited_nodes, distance_from_start, came_from,
                                                          visited_nodes]
        for neighbor in find_neighbors(grid, *current):
            x, y = neighbor
            if grid[x][y] == 3:
                continue

            if neighbor not in unvisited_nodes:
                continue

            tentative_distance = distance_from_start[current] + d(current, neighbor)
            if tentative_distance < distance_from_start[neighbor]:
                came_from[neighbor] = current
                distance_from_start[neighbor] = tentative_distance
        return 1, recunstruct_path(came_from, current), [unvisited_nodes, distance_from_start, came_from, visited_nodes]

    # Check if algorithm complete or failed
    if goal in came_from.keys():
        return 0, recunstruct_path(came_from, goal), [unvisited_nodes, distance_from_start, came_from, visited_nodes]

    # No solution
    else:
        return -1, None, [unvisited_nodes, distance_from_start, came_from, visited_nodes]


if __name__ == '__main__':
    m = [[0 for i in range(7)] for j in range(7)]
    print_grid(m)
    start = (0, 0)
    goal = (6, 6)
    print(distance((0, 0), (0, 1)))
    p = dijkstra(m, start, goal, distance)
    args = p[2]
    print(p)
    while p[0] != -1:
        if p[0] == 0:
            print('Final path', p[1])
            break

        p = dijkstra(m, start, goal, distance, args)
        print(p[0])
        args = p[2]

    print('QUIT')
