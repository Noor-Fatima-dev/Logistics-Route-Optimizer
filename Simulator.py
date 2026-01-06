import pygame
import math
import random

pygame.init()

random.seed(80)
# 42

# starting variables
WIDTH, HEIGHT = 600, 600
CELL = 10
ROWS = HEIGHT // CELL
COLS = WIDTH // CELL
NODES = ROWS * COLS

ROAD = 0
PLAIN = 1    
HOUSE = 2         
HIGHWAY = 3
OBSTACLE = 4      
SELECTED = 5      
PATH = 6
TRAFFIC = 7

dot_row, dot_col = ROWS - 6, 2
target_row, target_col = 2, COLS - 3


COLORS = {
    ROAD: (255, 255, 255),       # white
    PLAIN: (210, 180, 140),   # Tan
    HOUSE: (85, 140, 85),        # Green
    HIGHWAY: (255, 140, 0),      # Orange
    OBSTACLE: (200, 100, 50),     # Dark orange
    SELECTED: (0, 0, 255),      # Yellow
    PATH: (3, 243, 253),      # Light Blue
    TRAFFIC: (150, 150, 150)     # Gray
}

# Global Arrays
inf = math.inf
houses = []
path = []
adj = [[1000]*NODES for i in range(NODES)]
city_map = [[PLAIN for _ in range(COLS)] for _ in range(ROWS)]



screen = pygame.display.set_mode((WIDTH, HEIGHT+50))
pygame.display.set_caption("City Graph")

running = True
clock = pygame.time.Clock()

def to_pixel(row, col):
    return col * CELL + CELL // 2, row * CELL + CELL // 2

def node_id(r, c):
    return r * COLS + c

def rc_from_node(node):
    return node // COLS, node % COLS


# Arrays and Variables for Dijkstra's algorithm
parentNode = [[None for i in range(COLS)] for j in range(ROWS)]
dist = [[inf for i in range(COLS)] for j in range(ROWS)]
visited = [[False for i in range(COLS)] for j in range(ROWS)]
selectedNodes = [] # Nodes to target

# ------------------ MAZE MAP ------------------

# PLAIN by default
for r in range(ROWS):
    for c in range(COLS):
        city_map[r][c] = PLAIN

STEP = 2

# Recursive backtracking
def carve_maze(r, c):
    directions = [(STEP,0), (-STEP,0), (0,STEP), (0,-STEP)]
    random.shuffle(directions)

    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 1 <= nr < ROWS-1 and 1 <= nc < COLS-1:
            if city_map[nr][nc] == PLAIN:
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
        if city_map[r][c] == PLAIN:
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

    if city_map[r][c] == PLAIN:
        # So that house can touch a road
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
                    adj[u][v] = 2.0      # Can deliver here
                elif neighbor_type == OBSTACLE:
                    adj[u][v] = 1000      # Cannot pass
                elif neighbor_type == PLAIN:
                    adj[u][v] = 5.0      # Expensive

city_map[target_row][target_col] = ROAD 
city_map[dot_row][dot_col] = ROAD



source = node_id(dot_row, dot_col)
targetNode = source
#-----------------------calc-----------------------------
def DijkstraAlgo():
    global targetNode, parentNode, dist, visited, selectedNodes, source

    parentNode = [[None for i in range(COLS)] for j in range(ROWS)]
    dist = [[inf for i in range(COLS)] for j in range(ROWS)]
    visited = [[False for i in range(COLS)] for j in range(ROWS)]

    current = targetNode
    tr, tc = rc_from_node(targetNode)

    dist[tr][tc] = 0

    shortestDist = 100
    while current not in selectedNodes:

        cr, cc = rc_from_node(current)

        # Relax neighbors
        for v in range(NODES):
            if adj[current][v] < 1000:
                nr, nc = rc_from_node(v)

                if visited[nr][nc]:
                    continue

                newDist = dist[cr][cc] + adj[current][v]

                if newDist < dist[nr][nc]:
                    dist[nr][nc] = newDist
                    parentNode[nr][nc] = current

        # Mark current as FINAL
        visited[cr][cc] = True

        # Pick next node 
        shortestDist = inf    # minimum distance out of all unvisited nodes
        nextNode = None

        for i in range(ROWS):
            for j in range(COLS):
                if not visited[i][j] and dist[i][j] < shortestDist:
                    shortestDist = dist[i][j]
                    nextNode = node_id(i, j)

        if nextNode is None:
            break  # No path exists

        current = nextNode
        targetNode = current

path = []
def pathRetrace():
    global  targetNode, source, path

    target_row, target_col = rc_from_node(targetNode)
    r, c = target_row, target_col
    segment = []

    while node_id(r, c) != source:
        segment.append((r, c))
        r, c = rc_from_node(parentNode[r][c])
    segment.reverse()
    path.extend(segment)



a=0
start = False
path = [(dot_row, dot_col)]
pathTrail = []
dragging = False
warehouseX = dot_row
warehouseY = dot_col


# ------------------------------------- Main loop ---------------------------------------
while running:
    screen.fill((210, 180, 140))

    pathTrail.append((dot_row, dot_col))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            length = len(selectedNodes)
            if event.key == pygame.K_SPACE:
                start = True
                for i in range(length+1):
                    DijkstraAlgo()
                    pathRetrace()
                    selectedNodes.pop(selectedNodes.index(targetNode))
                    # for s in path:
                    #     print(s)
                    source = targetNode
                    if i == length-1:
                        selectedNodes.append(node_id(dot_row, dot_col))

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            
            col = mx // CELL
            row = my // CELL
           
            if city_map[row][col] == HOUSE:
                node = node_id(row, col)
                if node not in selectedNodes:
                    selectedNodes.append(node)
                    city_map[row][col] = SELECTED


            elif city_map[row][col] == ROAD or city_map[row][col] == HIGHWAY:
                node = node_id(row, col)
                dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                x, y = event.pos
                col = x // CELL
                row = y // CELL
                if city_map[row][col] == ROAD or city_map[row][col] == HIGHWAY:
                    city_map[row][col] = TRAFFIC
                    u = node_id(row, col)
                    directions = [(0,1), (-1,0), (0,-1), (1,0)]
                    for d in directions:
                        rowN, colN = row+d[0] , col+d[1]
                        if 0 <= rowN < ROWS and 0 <= colN < COLS:
                            v = node_id(rowN, colN)
                            neighbor_type = city_map[rowN][colN]
                            if neighbor_type == ROAD or neighbor_type == TRAFFIC or neighbor_type == HIGHWAY:
                                adj[u][v] = 2.5    




    # current = node_id(dot_row, dot_col)
    # neighbors = []
    # for v in range(NODES):
    #     if adj[current][v] != 1000 and rc_from_node(v) not in path:
    #         neighbors.append(rc_from_node(v))
    
    if start:
        if a < len(path):
            dot_row, dot_col = path[a]
            a += 1

    # Draw the city grid
    for r in range(ROWS):
        for c in range(COLS):
            cell_type = city_map[r][c]
            color = COLORS[cell_type]
            rect_pos = (c * CELL, r * CELL, CELL, CELL)
            pygame.draw.rect(screen, color, rect_pos)
            # Thin dark border for definition
            if(cell_type == ROAD or cell_type == HIGHWAY or cell_type == PATH or cell_type == TRAFFIC):
                pygame.draw.rect(screen, (210, 180, 140), rect_pos, 1)




    # ----------------------------- Simulation ------------------------------
    # Draw path 
    cost = 0
    for i in range(len(path)): 
        x, y = path[i]
        if(city_map[x][y] != SELECTED):
            city_map[x][y] = PATH
            if i+1 < len(path):
                cost += adj[node_id(x, y)][node_id(path[i+1][0], path[i+1][1] )]
                



    # Draw path trail
    for i in pathTrail: 
        x, y = i
        pygame.draw.circle(screen, (6, 135, 251), to_pixel(x, y), 3)

    # # Draw target
    # tx, ty = to_pixel(target_row, target_col)
    # pygame.draw.circle(screen, (0, 255, 0), (tx, ty), 6)
    # pygame.draw.circle(screen, (255, 255, 255), (tx, ty), 6, 2)

    # Draw Logistics Van
    ax, ay = to_pixel(dot_row, dot_col)
    pygame.draw.circle(screen, (255, 0, 0), (ax, ay), 5)
    pygame.draw.circle(screen, (255, 255, 255), (ax, ay), 5, 1)

    # Warehouse Location

    wx, wy = to_pixel(warehouseX, warehouseY)
    pygame.draw.circle(screen, (255, 0, 0), (wx, wy), 8, 1)



    # Write Text
    font = pygame.font.Font(None, 20)
    text_surface = font.render(f"Current Position: ({dot_row}, {dot_col})", True, (255, 255, 255))
    screen.blit(text_surface, (10, HEIGHT))
    text_surface = font.render(f"Total Cost: {cost}", True, (255, 255, 255))
    screen.blit(text_surface, (10, HEIGHT+15))

    pygame.display.update()
    clock.tick(10)

pygame.quit()
