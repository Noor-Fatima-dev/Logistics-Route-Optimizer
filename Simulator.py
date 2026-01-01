import pygame
import math
import random

pygame.init()

random.seed(42)

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

dot_row, dot_col = ROWS - 3, 2
target_row, target_col = 2, COLS - 3

# Updated colors to match the image
COLORS = {
    ROAD: (255, 255, 255),      # Cream/wheat color for roads
    BUILDING: (210, 180, 140),   # Tan for buildings (darker than roads)
    HOUSE: (85, 140, 85),        # Green for houses
    HIGHWAY: (255, 140, 0),      # Orange for highway
    OBSTACLE: (200, 100, 50)     # Dark orange for obstacles
}

inf = math.inf
houses = []
path = []
adj = [[inf]*NODES for i in range(NODES)]
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
                    adj[u][v] = 0.5      # Fast/cheap
                elif neighbor_type == HOUSE:
                    adj[u][v] = 1.0      # Can deliver here
                elif neighbor_type == OBSTACLE:
                    adj[u][v] = inf      # Cannot pass
                elif neighbor_type == BUILDING:
                    adj[u][v] = 3.0      # Expensive






# ------------------------- CITY MAP ---------------------------

# Initialize everything as buildings
for r in range(ROWS):
    for c in range(COLS):
        city_map[r][c] = BUILDING

# Create winding maze-like roads
# Vertical roads that snake and branch
for c in [8, 16, 24, 32, 40, 48]:
    shift = 0
    for r in range(ROWS):
        # Random drift and branching
        if random.random() < 0.2:
            shift += random.choice([-2, -1, 0, 1, 2])
            shift = max(-4, min(4, shift))
        
        if 0 <= c + shift < COLS:
            city_map[r][c + shift] = ROAD
            
            # Random horizontal branches
            if random.random() < 0.15:
                branch_len = random.randint(2, 6)
                direction = random.choice([-1, 1])
                for b in range(branch_len):
                    if 0 <= c + shift + (b * direction) < COLS:
                        city_map[r][c + shift + (b * direction)] = ROAD

# Horizontal roads that snake and branch
for r in [6, 14, 22, 30, 38, 46, 54]:
    shift = 0
    for c in range(COLS):
        # Random drift and branching
        if random.random() < 0.2:
            shift += random.choice([-2, -1, 0, 1, 2])
            shift = max(-4, min(4, shift))
        
        if 0 <= r + shift < ROWS:
            city_map[r + shift][c] = ROAD
            
            # Random vertical branches
            if random.random() < 0.15:
                branch_len = random.randint(2, 6)
                direction = random.choice([-1, 1])
                for b in range(branch_len):
                    if 0 <= r + shift + (b * direction) < ROWS:
                        city_map[r + shift + (b * direction)][c] = ROAD

# Add many winding alleys and dead-ends
for _ in range(50):
    r = random.randint(3, ROWS - 4)
    c = random.randint(3, COLS - 4)
    length = random.randint(3, 8)
    direction = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
    
    for i in range(length):
        rr = r + i * direction[0]
        cc = c + i * direction[1]
        
        # Random turns in the alley
        if random.random() < 0.3:
            direction = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
        
        if 0 <= rr < ROWS and 0 <= cc < COLS and city_map[rr][cc] == BUILDING:
            city_map[rr][cc] = ROAD

# Create winding highway with gaps
highway_col = COLS // 2 + random.randint(-8, 8)
shift = 0

for r in range(ROWS):
    # Highway meanders
    if random.random() < 0.12:
        shift += random.choice([-1, 0, 0, 1])
        shift = max(-3, min(3, shift))
    
    col = highway_col + shift
    
    if 0 <= col < COLS:
        # Make highway 2-3 cells wide
        width = random.choice([2, 2, 3])
        for w in range(width):
            if 0 <= col + w < COLS:
                city_map[r][col + w] = HIGHWAY
    
    # Random gaps and obstacles in highway
    if random.random() < 0.06:
        if 0 <= col < COLS:
            city_map[r][col] = OBSTACLE

# Add random obstacle blocks scattered around
for _ in range(25):
    r = random.randint(3, ROWS - 4)
    c = random.randint(3, COLS - 4)
    
    # Create irregular obstacle shapes
    shape = random.choice(['line', 'block', 'L'])
    
    if shape == 'line':
        length = random.randint(2, 5)
        direction = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
        for i in range(length):
            rr, cc = r + i*direction[0], c + i*direction[1]
            if 0 <= rr < ROWS and 0 <= cc < COLS:
                city_map[rr][cc] = OBSTACLE
    
    elif shape == 'block':
        size = random.randint(1, 3)
        for dr in range(size):
            for dc in range(size):
                if 0 <= r+dr < ROWS and 0 <= c+dc < COLS:
                    city_map[r+dr][c+dc] = OBSTACLE
    
    else:  # L-shape
        length = random.randint(2, 4)
        for i in range(length):
            if 0 <= r+i < ROWS and 0 <= c < COLS:
                city_map[r+i][c] = OBSTACLE
            if 0 <= r < ROWS and 0 <= c+i < COLS:
                city_map[r][c+i] = OBSTACLE

# ---------------- HOUSES (Green blocks) ----------------

houses = []
attempts = 0

while len(houses) < 15 and attempts < 300:
    r = random.randint(2, ROWS - 3)
    c = random.randint(2, COLS - 3)

    if city_map[r][c] == BUILDING:
        # Must be adjacent to a road
        adjacent_to_road = any(
            0 <= r+dr < ROWS and 0 <= c+dc < COLS and city_map[r+dr][c+dc] == ROAD
            for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]
        )
        if adjacent_to_road:
            # Create 2x2 house blocks for better visibility
            can_place = True
            for dr in range(2):
                for dc in range(2):
                    if r+dr >= ROWS or c+dc >= COLS or city_map[r+dr][c+dc] not in [BUILDING, HOUSE]:
                        can_place = False
            
            if can_place:
                for dr in range(2):
                    for dc in range(2):
                        city_map[r+dr][c+dc] = HOUSE
                houses.append((r, c))
    attempts += 1




# Main loop
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current = node_id(dot_row, dot_col)
    neighbors = []
    for v in range(NODES):
        if adj[current][v] == 1:
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

    # Update path
    if len(neighbors) > 0:
        path.append((dot_row, dot_col))
        dot_row, dot_col = random.choice(neighbors)

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
    clock.tick(8)

pygame.quit()