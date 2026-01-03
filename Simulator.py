import pygame
import math
import random

pygame.init()

random.seed(42)
# 42

WIDTH, HEIGHT = 600, 600
CELL = 10
ROWS = HEIGHT // CELL
COLS = WIDTH // CELL
NODES = ROWS * COLS

ROAD = 0
BUILDING = 1    
HOUSE = 2         
HIGHWAY = 3
OBSTACLE = 4      

dot_row, dot_col = ROWS - 6, 2
target_row, target_col = 2, COLS - 3


COLORS = {
    ROAD: (255, 255, 255),      # white
    BUILDING: (210, 180, 140),   # Tan
    HOUSE: (85, 140, 85),        # Green
    HIGHWAY: (255, 140, 0),      # Orange
    OBSTACLE: (200, 100, 50)     # Dark orange
}

inf = math.inf
houses = []
path = []
adj = [[1000]*NODES for i in range(NODES)]
city_map = [[BUILDING for _ in range(COLS)] for _ in range(ROWS)]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("City Graph")

running = True
clock = pygame.time.Clock()

def to_pixel(row, col):
    return col * CELL + CELL // 2, row * CELL + CELL // 2

def node_id(r, c):
    return r * COLS + c

def rc_from_node(node):
    return node // COLS, node % COLS




# ------------------ MAZE MAP ------------------

# BUILDING by default
for r in range(ROWS):
    for c in range(COLS):
        city_map[r][c] = BUILDING

STEP = 2

# Recursive backtracking
def carve_maze(r, c):
    directions = [(STEP,0), (-STEP,0), (0,STEP), (0,-STEP)]
    random.shuffle(directions)

    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 1 <= nr < ROWS-1 and 1 <= nc < COLS-1:
            if city_map[nr][nc] == BUILDING:
                city_map[r + dr//2][c + dc//2] = ROAD 
                city_map[nr][nc] = ROAD
                carve_maze(nr, nc)

start_r = random.randrange(1, ROWS, STEP)
start_c = random.randrange(1, COLS, STEP)
city_map[start_r][start_c] = ROAD
carve_maze(start_r, start_c)

# Fusion

for r in range(2, ROWS-2):
    for c in range(2, COLS-2):
        if city_map[r][c] == BUILDING:
            if random.random() < 0.15:
                city_map[r][c] = ROAD

# 2 Highways

mid = ROWS // 2 - CELL*2
for c in range(COLS):
    city_map[mid][c] = HIGHWAY
    if mid+1 < ROWS:
        city_map[mid+1][c] = HIGHWAY

mid = COLS // 2 + CELL*2
for r in range(ROWS):
    city_map[r][mid] = HIGHWAY
    if mid+1 < COLS:
        city_map[r][mid+1] = HIGHWAY

# ------------------ OBSTACLES ------------------

for _ in range(20):
    r = random.randint(2, ROWS-3)
    c = random.randint(2, COLS-3)
    city_map[r][c] = OBSTACLE

# ------------------ HOUSES ------------------

houses = []
attempts = 0

while len(houses) < 12 and attempts < 300:
    r = random.randint(2, ROWS-3)
    c = random.randint(2, COLS-3)

    if city_map[r][c] == BUILDING:
        # must touch a road
        if any(
            0 <= r+dr < ROWS and 0 <= c+dc < COLS and city_map[r+dr][c+dc] == ROAD
            for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]
        ):
            city_map[r][c] = HOUSE
            houses.append((r, c))
    attempts += 1


# Adjacency matrix
for r in range(ROWS):
    for c in range(COLS):
        u = node_id(r, c)
        cell_type = city_map[r][c]

        directions = [(0,1), (-1,0), (0,-1), (1,0)]

        for d in directions:
            rowN, colN = r+d[0] , c+d[1]

            if 0 <= rowN < ROWS and 0 <= colN < COLS:

                v = node_id(rowN, colN)
                neighbor_type = city_map[rowN][colN]

                if neighbor_type == ROAD:
                    adj[u][v] = 1.0      # Normal cost
                elif neighbor_type == HIGHWAY:
                    adj[u][v] = 0.5      # Cheap
                elif neighbor_type == HOUSE:
                    adj[u][v] = 1.0      # Can deliver here
                elif neighbor_type == OBSTACLE:
                    adj[u][v] = 1000      # Cannot pass
                elif neighbor_type == BUILDING:
                    adj[u][v] = 5.0      # Expensive



# Main loop
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current = node_id(dot_row, dot_col)
    neighbors = []
    for v in range(NODES):
        if adj[current][v] != 1000 and rc_from_node(v) not in path:
            neighbors.append(rc_from_node(v))

    # Draw the city grid
    for r in range(ROWS):
        for c in range(COLS):
            cell_type = city_map[r][c]
            color = COLORS[cell_type]
            rect_pos = (c * CELL, r * CELL, CELL, CELL)
            pygame.draw.rect(screen, color, rect_pos)
            # Thin dark border for definition
            if(cell_type == ROAD or cell_type == HIGHWAY):
                pygame.draw.rect(screen, (210, 180, 140), rect_pos, 1)

    neighborWeights = []
    for v in range(NODES):
        if adj[current][v] != 1000:
            neighborWeights.append(adj[current][v])

    # Update path
    if len(neighbors) > 0:
        path.append((dot_row, dot_col))
        min_index = neighborWeights.index(min(neighborWeights))
        dot_row, dot_col = neighbors[min_index]

    # Draw path trail
    for i in path: 
        x, y = i
        pygame.draw.circle(screen, (0, 200, 200), to_pixel(x, y), 2)

    # Draw target
    tx, ty = to_pixel(target_row, target_col)
    pygame.draw.circle(screen, (0, 255, 0), (tx, ty), 6)
    pygame.draw.circle(screen, (255, 255, 255), (tx, ty), 6, 2)

    # Draw Logistics Van
    ax, ay = to_pixel(dot_row, dot_col)
    pygame.draw.circle(screen, (255, 0, 0), (ax, ay), 5)
    pygame.draw.circle(screen, (255, 255, 255), (ax, ay), 5, 1)

    pygame.display.update()
    clock.tick(1)

pygame.quit()
