import pygame
import sys
import random
import automata_generator
import miner
import search

# --- CONFIGURATION ---
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 10
COLS = WIDTH // TILE_SIZE
ROWS = HEIGHT // TILE_SIZE

COLOR_WALL = (20, 20, 20)      
COLOR_FLOOR = (200, 200, 200)  
COLOR_GRID = (50, 50, 50)      

# --- INITIALIZATION ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Dungeon Master - Final Natural Cave")
clock = pygame.time.Clock()

# --- THE DATA (NATURAL CAVE PIPELINE) ---

path = None
grid_map = []
start_pos = (0,0)
end_pos = (0,0)

# Keep regenerating until we get a solvable map
attempts = 0
while path is None:
    attempts += 1
    print(f"Generation Attempt {attempts}...")

# 1. Generate Rooms (High density for small rooms)
    base_grid = automata_generator.generate_cave(ROWS, COLS, iterations=2, fill_percent=0.80)

    # 2. Connect Rooms (Miner digs '2's)
    connected_grid = miner.mine_tunnels(base_grid)

    # 3. Smooth (Respects '2's, erodes walls around them)
    smoothed_grid = automata_generator.generate_cave(ROWS, COLS, iterations=2, input_grid=connected_grid)

    # 4. CLEANUP: Convert all '2's back to '1's
    grid_map = []
    for r in range(ROWS):
        new_row = []
        for c in range(COLS):
            if smoothed_grid[r][c] == 2:
                new_row.append(1) # Convert Tunnel -> Floor
            else:
                new_row.append(smoothed_grid[r][c])
        grid_map.append(new_row)

    # 5. Pick Start/End
    # Find all valid floor tiles
    floors = []
    for r in range(ROWS):
        for c in range(COLS):
            if grid_map[r][c] == 1:
                floors.append((r, c))
    
    # If map is somehow empty, retry
    if len(floors) < 2:
        continue

    start_pos = random.choice(floors)
    end_pos = random.choice(floors)
    
    # Ensure start and end are different
    while end_pos == start_pos:
        end_pos = random.choice(floors)

    # 5. THE CHECK: Verify Path
    path = search.astar(grid_map, start_pos, end_pos)

print(f"Success! Map generated in {attempts} attempts.")

# --- DRAWING FUNCTION ---
def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            
            tile_type = grid_map[row][col]
            if tile_type == 1:
                color = COLOR_FLOOR
            else:
                color = COLOR_WALL
            
            # Draw base tile
            pygame.draw.rect(screen, color, (x, y, TILE_SIZE, TILE_SIZE))
            # pygame.draw.rect(screen, COLOR_GRID, (x, y, TILE_SIZE, TILE_SIZE), 1)

    # --- Draw Path ---
    if path:
        for (r, c) in path:
            x = c * TILE_SIZE
            y = r * TILE_SIZE
            center_offset = TILE_SIZE // 4
            pygame.draw.rect(screen, (0, 0, 255), (x + center_offset, y + center_offset, TILE_SIZE//2, TILE_SIZE//2))

    # --- Draw Start & End ---
    sx, sy = start_pos[1] * TILE_SIZE, start_pos[0] * TILE_SIZE
    pygame.draw.rect(screen, (0, 255, 0), (sx, sy, TILE_SIZE, TILE_SIZE))

    ex, ey = end_pos[1] * TILE_SIZE, end_pos[0] * TILE_SIZE
    pygame.draw.rect(screen, (255, 0, 0), (ex, ey, TILE_SIZE, TILE_SIZE))

# --- MAIN LOOP ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    screen.fill(COLOR_WALL) 
    draw_grid()             
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()