import pygame
import sys
import generator
import random
import search
import automata_generator
import miner

# --- CONFIGURATION ---
# Screen dimensions
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 10

# Calculate how many tiles fit on screen
COLS = WIDTH // TILE_SIZE
ROWS = HEIGHT // TILE_SIZE

# Colors (R, G, B)F
COLOR_WALL = (20, 20, 20)      # Dark Grey
COLOR_FLOOR = (200, 200, 200)  # Light Grey
COLOR_GRID = (50, 50, 50)      # For grid lines

# --- INITIALIZATION ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Dungeon Master - Milestone 1")
clock = pygame.time.Clock()

# --- THE DATA ---

#This is the drunken walk, bad idea but a good baseline to start building from
#grid_map = generator.generate_drunken_walk(ROWS, COLS, max_steps=10000)

path = None
grid_map = []
start_pos = (0,0)
end_pos = (0,0)

# Keep regenerating until we get a solvable map
attempts = 0
while path is None:
    attempts += 1
    print(f"Generation Attempt {attempts}...")

    # 1. Generate Rooms (The Cheese)
    room_grid = automata_generator.generate_cave(ROWS, COLS, iterations=5, fill_percent=0.65)

    # 2. Connect Rooms (The Guided Miner)
    # We use fewer tunnels now because they are targeted and effective
    grid_map = miner.mine_tunnels(room_grid)

    # 3. Pick Start/End
    # (Simple logic: Pick random floor tiles)
    while True:
        sr, sc = random.randint(0, ROWS-1), random.randint(0, COLS-1)
        if grid_map[sr][sc] == 1:
            start_pos = (sr, sc)
            break
    
    while True:
        er, ec = random.randint(0, ROWS-1), random.randint(0, COLS-1)
        if grid_map[er][ec] == 1 and (er,ec) != start_pos:
            end_pos = (er, ec)
            break

    # 4. THE CHECK: Does a path exist?
    # If this returns a list, the loop breaks. If None, it repeats.
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
            #pygame.draw.rect(screen, COLOR_GRID, (x, y, TILE_SIZE, TILE_SIZE), 1)

    # --- Draw Path ---
    if path:
        for (r, c) in path:
            x = c * TILE_SIZE
            y = r * TILE_SIZE
            # Draw a smaller blue square for the path
            center_offset = TILE_SIZE // 4
            pygame.draw.rect(screen, (0, 0, 255), (x + center_offset, y + center_offset, TILE_SIZE//2, TILE_SIZE//2))

    # --- Draw Start & End ---
    # Start = Green
    sx, sy = start_pos[1] * TILE_SIZE, start_pos[0] * TILE_SIZE
    pygame.draw.rect(screen, (0, 255, 0), (sx, sy, TILE_SIZE, TILE_SIZE))

    # End = Red
    ex, ey = end_pos[1] * TILE_SIZE, end_pos[0] * TILE_SIZE
    pygame.draw.rect(screen, (255, 0, 0), (ex, ey, TILE_SIZE, TILE_SIZE))
# --- MAIN LOOP ---
running = True
while running:
    # 1. Event Handling (Input)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # 2. Drawing
    screen.fill(COLOR_WALL) # Clear screen
    draw_grid()             # Draw our map
    
    # 3. Update Display
    pygame.display.flip()
    clock.tick(60) # Limit to 60 FPS

pygame.quit()
sys.exit()