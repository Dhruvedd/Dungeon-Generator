import random
from collections import deque

def get_regions(grid, rows, cols):
    """
    Uses Flood Fill to find all distinct disconnected regions of floor tiles.
    Returns a list of regions, where each region is a list of (r, c) tuples.
    """
    regions = []
    visited = set()

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and (r, c) not in visited:
                # Found a new region! Flood fill to find all its tiles.
                new_region = []
                queue = deque([(r, c)])
                visited.add((r, c))
                
                while queue:
                    curr_r, curr_c = queue.popleft()
                    new_region.append((curr_r, curr_c))
                    
                    # Check neighbors
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        if 0 <= nr < rows and 0 <= nc < cols:
                            if grid[nr][nc] == 1 and (nr, nc) not in visited:
                                visited.add((nr, nc))
                                queue.append((nr, nc))
                                
                regions.append(new_region)
    
    return regions

def mine_tunnels(input_grid, max_tunnels=15): # max_tunnels ignored here, we dig as needed
    """
    Connects ALL disconnected regions to the largest region.
    """
    rows = len(input_grid)
    cols = len(input_grid[0])
    grid = [row[:] for row in input_grid] # Copy grid

    # 1. Identify all separate rooms/regions
    regions = get_regions(grid, rows, cols)
    
    if len(regions) <= 1:
        return grid # Already fully connected!

    # 2. Sort regions by size (Largest is last)
    regions.sort(key=len)
    main_hub = regions[-1] # The biggest room is our target
    isolated_regions = regions[:-1] # All the small islands

    # 3. Connect every isolated region to the Main Hub
    for region in isolated_regions:
        # Pick a random point in the small island
        start = random.choice(region)
        # Pick a random point in the Main Hub
        end = random.choice(main_hub)
        
        # DIG THE TUNNEL (Guided Drunkard Style)
        current_r, current_c = start
        target_r, target_c = end
        
        while (current_r, current_c) != (target_r, target_c):
            # Determine moves
            move_r = 0
            move_c = 0
            
            if current_r < target_r: move_r = 1
            elif current_r > target_r: move_r = -1
            
            if current_c < target_c: move_c = 1
            elif current_c > target_c: move_c = -1
            
            # Wiggle Logic (High bias to target to ensure we actually connect)
            if random.random() < 0.85: # 85% focus, 15% noise
                if move_r != 0 and move_c != 0:
                    if random.random() < 0.5: current_r += move_r
                    else: current_c += move_c
                elif move_r != 0: current_r += move_r
                elif move_c != 0: current_c += move_c
            else:
                # Random noise
                directions = [(-1,0), (1,0), (0,-1), (0,1)]
                dr, dc = random.choice(directions)
                current_r += dr
                current_c += dc
            
            # Clamp bounds
            current_r = max(1, min(rows-2, current_r))
            current_c = max(1, min(cols-2, current_c))
            
            # Carve
            grid[current_r][current_c] = 1

    return grid