import pygame
import sys
import generator

# --- CONFIGURATION ---
# Screen dimensions
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 5

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

# --- THE DATA (Your AI's World) ---
# Generate the map using our new algorithm
# We pass ROWS and COLS so it knows how big the map is

grid_map = generator.generate_drunken_walk(ROWS, COLS, max_steps=10000)

# --- DRAWING FUNCTION ---
def draw_grid():
    """Reads the grid_map and draws tiles accordingly."""
    for row in range(ROWS):
        for col in range(COLS):
            # Calculate the screen position (x, y)
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            
            # Determine color based on data
            tile_type = grid_map[row][col]
            if tile_type == 1:
                color = COLOR_FLOOR
            else:
                color = COLOR_WALL
            
            # Draw the tile
            pygame.draw.rect(screen, color, (x, y, TILE_SIZE, TILE_SIZE))
            
            # Draw a faint border (optional, helps visualize the grid)
            pygame.draw.rect(screen, COLOR_GRID, (x, y, TILE_SIZE, TILE_SIZE), 1)

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