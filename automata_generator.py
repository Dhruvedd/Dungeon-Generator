import random

def generate_cave(rows, cols, iterations=5, fill_percent=0.50, input_grid=None):
    if input_grid is None:
        grid = []
        for r in range(rows):
            row = []
            for c in range(cols):
                if r == 0 or r == rows-1 or c == 0 or c == cols-1:
                    row.append(0) 
                else:
                    if random.random() < fill_percent:
                        row.append(0)
                    else:
                        row.append(1)
            grid.append(row)
    else:
        grid = [row[:] for row in input_grid]

    for i in range(iterations):
        grid = apply_automata_rules(grid, rows, cols)
        
    return grid

def apply_automata_rules(old_grid, rows, cols):
    new_grid = [[0 for _ in range(cols)] for _ in range(rows)]
    
    for r in range(rows):
        for c in range(cols):
            # Border Constraint
            if r == 0 or r == rows-1 or c == 0 or c == cols-1:
                new_grid[r][c] = 0
                continue

            # --- THE PROTECTION FIX ---
            # If this tile is a Tunnel (2), KEEP IT A TUNNEL.
            # Do not apply wall logic to it.
            if old_grid[r][c] == 2:
                new_grid[r][c] = 2
                continue
            # --------------------------

            wall_neighbors = count_walls(old_grid, r, c, rows, cols)
            
            # Standard Physics
            if wall_neighbors >= 5: # wall logic
                new_grid[r][c] = 0
            elif wall_neighbors <= 4: # floor logic
                 new_grid[r][c] = 1
            else:
                new_grid[r][c] = old_grid[r][c]
                
    return new_grid

def count_walls(grid, r, c, rows, cols):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0: continue
            nr, nc = r + i, c + j
            
            if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
                count += 1
            # Note: 2 counts as Floor (not wall), so we only check for 0
            elif grid[nr][nc] == 0:
                count += 1
    return count