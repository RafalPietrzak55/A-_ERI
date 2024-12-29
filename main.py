import math

def load_grid(filename):
    with open(filename, 'r') as file:
        grid = [list(map(int, line.strip().split())) for line in file]
    return grid

def heuristic(a, b):
    """Oblicza odległość euklidesową jako heurystykę."""
    x1, y1 = a
    x2, y2 = b
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def get_neighbors(node, grid):
    """Znajduje wszystkie możliwe sąsiadujące pola dla aktualnego węzła."""
    neighbors = []
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # prawo, lewo, dół, góra
    for dx, dy in directions:
        x, y = node[0] + dx, node[1] + dy
        if 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] == 0:
            neighbors.append((x, y))
    return neighbors

def reconstruct_path(came_from, current):
    """Odtwarza ścieżkę od celu do początku."""
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path

def a_star(grid, start, goal):
    """Wykonuje algorytm A* na zadanej siatce."""
    open_set = {start}
    came_from = {}

    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        # Znajdź węzeł o najniższym f_score
        current = min(open_set, key=lambda node: f_score.get(node, float('inf')))

        if current == goal:
            return reconstruct_path(came_from, current)

        open_set.remove(current)

        for neighbor in get_neighbors(current, grid):
            tentative_g_score = g_score[current] + 1

            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                if neighbor not in open_set:
                    open_set.add(neighbor)

    return None  # Brak znalezionej ścieżki

def print_grid_with_path(grid, path):
    """Wyświetla siatkę z zaznaczoną ścieżką."""
    for x, y in path:
        grid[x][y] = 3

    for row in grid:
        print(' '.join(str(cell) for cell in row))

if __name__ == "__main__":
    grid = load_grid("grid.txt")
    start = (19, 0)  # Pozycja startowa
    goal = (0, 19)  # Pozycja końcowa

    path = a_star(grid, start, goal)

    if path:
        print("Znaleziono ścieżkę:")
        print(path)
        print("Siatka z wyznaczoną ścieżką:")
        print_grid_with_path(grid, path)
    else:
        print("Nie znaleziono ścieżki.")
