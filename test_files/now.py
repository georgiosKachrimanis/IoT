import math


def calculate_distances(points):
    n = len(points)
    distances = [[0 for j in range(n)] for i in range(n)]

    for i in range(n):
        name1, (x1, y1) = list(points[i].items())[0]
        for j in range(i + 1, n):
            name2, (x2, y2) = list(points[j].items())[0]
            dx = abs(x2 - x1)
            dy = abs(y2 - y1)
            distance = math.sqrt(dx * dx + dy * dy)
            distances[i][j] = distance
            distances[j][i] = distance

    row_totals = {}
    for i in range(n):
        name, _ = list(points[i].items())[0]
        row_total = sum(distances[i])
        row_totals[name] = row_total

    return row_totals


points = [{"Center": (0, 0)}, {"Pi4": (3, 2)}, {"pi3": (4, 1)}, {"pi2": (5, 4)}, {"pi5": (-3, 4)}, {"pi6": (-5, -4)},{"pi8": (-5, -5)},{"pi9": (-3, -2)},  {"pi7": (-2, -2)}]

row_totals = calculate_distances(points)

for name in row_totals:
    print("Total distance for point {}: {}".format(name, row_totals[name]))
