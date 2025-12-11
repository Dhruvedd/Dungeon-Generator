import random
from collections import deque

def get_regions(grid, rows, cols):
    """ Standard flood fill to find regions. """
    regions = []
    visited = set()

    for r in range(rows):
        for c in range(cols):
            # Treat both 1 (Room) and 2 (Tunnel) as walkables
            if grid[r][c] in [1, 2] and (r, c) not in visited:
                new_region = []
                queue = deque([(r, c)])
                visited.add((r, c))
                
                while queue:
                    curr_r, curr_c = queue.popleft()
                    new_region.append((curr_r, curr_c))
                    
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        if 0 <= nr < rows and 0 <= nc < cols:
                            if grid[nr][nc] in [1, 2] and (nr, nc) not in visited:
                                visited.add((nr, nc))
                                queue.append((nr, nc))
                                
                regions.append(new_region)
    return regions

def dig_tunnel(grid, start, end, rows, cols):
    """ Digs a standard 1-tile jagged tunnel, but marks it as '2'. """
    curr_r, curr_c = start
    target_r, target_c = end
    
    while (curr_r, curr_c) != (target_r, target_c):
        # 1. Determine Direction
        move_r = 0
        move_c = 0
        if curr_r < target_r: move_r = 1
        elif curr_r > target_r: move_r = -1
        if curr_c < target_c: move_c = 1
        elif curr_c > target_c: move_c = -1
        
        # 2. Move with noise
        if random.random() < 0.80:
            if move_r != 0 and move_c != 0:
                if random.random() < 0.5: curr_r += move_r
                else: curr_c += move_c
            elif move_r != 0: curr_r += move_r
            elif move_c != 0: curr_c += move_c
        else:
            directions = [(-1,0), (1,0), (0,-1), (0,1)]
            dr, dc = random.choice(directions)
            curr_r += dr
            curr_c += dc
            
        # 3. Clamp Bounds
        curr_r = max(1, min(rows-2, curr_r))
        curr_c = max(1, min(cols-2, curr_c))
        
        # 4. MARK AS PROTECTED FLOOR (2)
        grid[curr_r][curr_c] = 2

def mine_tunnels(input_grid):
    rows = len(input_grid)
    cols = len(input_grid[0])
    grid = [row[:] for row in input_grid] 

    # 1. Find regions
    regions = get_regions(grid, rows, cols)
    if len(regions) <= 1:
        return grid 

    # 2. Sort and Connect
    regions.sort(key=len)
    main_hub = regions[-1]
    islands = regions[:-1]

    for island in islands:
        start = random.choice(island)
        end = random.choice(main_hub)
        dig_tunnel(grid, start, end, rows, cols)

    return grid