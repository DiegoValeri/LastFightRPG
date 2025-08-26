import random
import heapq

def dig_room(x, y, w, h, grid):
    for i in range(y, y + h):
        for j in range(x, x + w):
            grid[i][j] = "▉"
            if i > 0 and grid[i-1][j] == "▇":
                grid[i][j] = "s"
            else:
                grid[i][j] = "▉"


def carve_corridor(grid, x1, y1, x2, y2):
    # couloir horizontal
    corridor_y = y1
    for x in range(min(x1, x2), max(x1, x2) + 1):
        grid[corridor_y][x] = "▉"

    # couloir vertical (largeur 2)
    if y1 != y2:
        end_x = x2
        for y in range(min(y1, y2), max(y1, y2) + 1):
            grid[y][end_x] = "▉"
            # on ajoute une 2ème colonne à droite si possible
            if end_x + 1 < len(grid[0]):
                grid[y][end_x + 1] = "▉"

def generate_structured_map(width=300, height=150, room_count=35):
    grid = [["▇" for _ in range(width)] for _ in range(height)]
    rooms = []

    # --- SALLE FORCÉE AUTOUR DE (5,5) ---
    forced_room_w = random.randint(6, 9)
    forced_room_h = random.randint(4, 6)
    forced_x = max(1, 5 - forced_room_w // 2)
    forced_y = max(1, 5 - forced_room_h // 2)

    rooms.append((forced_x, forced_y, forced_room_w, forced_room_h))
    dig_room(forced_x, forced_y, forced_room_w, forced_room_h, grid)

    # --- autres salles aléatoires ---
    min_distance = 11
    for _ in range(room_count - 1):
        for _ in range(50):
            w = random.randint(8, 10)
            h = random.randint(5, 7)
            x = random.randint(1, width - w - 2)
            y = random.randint(1, height - h - 2)

            cx, cy = x + w // 2, y + h // 2
            too_close = False
            for (rx, ry, rw, rh) in rooms:
                rcx, rcy = rx + rw // 2, ry + rh // 2
                dist = ((cx - rcx) ** 2 + (cy - rcy) ** 2) ** 0.5
                if dist < min_distance:
                    too_close = True
                    break

            if not too_close:
                rooms.append((x, y, w, h))
                dig_room(x, y, w, h, grid)
                break

    # --- MST pour connecter les salles ---
    centers = [(x + w//2, y + h//2) for (x, y, w, h) in rooms]
    n = len(centers)
    connected = {0}
    edges = []
    for j in range(1, n):
        cx1, cy1 = centers[0]
        cx2, cy2 = centers[j]
        dist = abs(cx1 - cx2) + abs(cy1 - cy2)
        heapq.heappush(edges, (dist, 0, j))

    while len(connected) < n:
        dist, i, j = heapq.heappop(edges)
        if j in connected:
            continue
        connected.add(j)
        carve_corridor(grid, *centers[i], *centers[j])
        for k in range(n):
            if k not in connected:
                cx1, cy1 = centers[j]
                cx2, cy2 = centers[k]
                dist = abs(cx1 - cx2) + abs(cy1 - cy2)
                heapq.heappush(edges, (dist, j, k))

    # --- portail ---
    spawn = (5, 5)
    farthest_portal, max_dist = None, -1
    for y in range(height):
        for x in range(width):
            if grid[y][x] == "▉":
                dist = abs(x - spawn[0]) + abs(y - spawn[1])
                if dist > max_dist:
                    max_dist = dist
                    farthest_portal = (x, y)

    if farthest_portal:
        px, py = farthest_portal
        grid[py][px] = "%"
    else:
        px, py = spawn

    # --- coffre ---
    farthest_chest, max_score = None, -1
    for y in range(height):
        for x in range(width):
            if grid[y][x] == "▉":
                dist_spawn = abs(x - spawn[0]) + abs(y - spawn[1])
                dist_portal = abs(x - px) + abs(y - py)
                score = dist_spawn + dist_portal
                if score > max_score:
                    max_score = score
                    farthest_chest = (x, y)

    if farthest_chest:
        cx, cy = farthest_chest
        grid[cy][cx] = "C"

    grid[5][5] = "▉"
    return ["".join(row) for row in grid]
