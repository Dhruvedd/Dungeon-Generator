import random

def mine_tunnels(input_grid, max_tunnels=50, max_length=15):
    """
    Digs long, narrow tunnels into an existing map to connect rooms.
    Uses 'Momentum' (straight lines) to avoid creating blobby rooms 
    or walking back on itself constantly.
    """
    # 1. Create a copy of the grid to work on
    rows = len(input_grid)
    cols = len(input_grid[0])
    grid = [row[:] for row in input_grid]

    # 2. Pick a random starting point that is already a FLOOR
    # We want to start from an existing room to ensure connectivity.
    start_r, start_c = rows // 2, cols // 2
    
    # Try 100 times to find a valid floor tile to start mining from
    for _ in range(100):
        r = random.randint(1, rows - 2)
        c = random.randint(1, cols - 2)
        if grid[r][c] == 1:
            start_r, start_c = r, c
            break

    current_r, current_c = start_r, start_c

    # 3. The Mining Loop
    for i in range(max_tunnels):
        
        # A. Pick a random direction
        # (row_change, col_change)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        dr, dc = random.choice(directions)
        
        # B. Decide how long to dig in this direction (Momentum)
        # Random length between 5 and max_length
        tunnel_len = random.randint(5, max_length)
        
        # C. Dig!
        for step in range(tunnel_len):
            # Calculate next step
            next_r = current_r + dr
            next_c = current_c + dc
            
            # Boundary Check (Leave a 1-tile border around map)
            if 1 <= next_r < rows - 1 and 1 <= next_c < cols - 1:
                current_r = next_r
                current_c = next_c
                
                # Turn wall into floor
                grid[current_r][current_c] = 1
            else:
                # Hit the edge? Stop this tunnel and pick a new direction
                break
        
        # After the tunnel is done, the miner stays at 'current_r, current_c'
        # and loops back to pick a NEW direction from there.

    return grid