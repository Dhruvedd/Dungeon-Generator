import random

def mine_tunnels(input_grid, max_tunnels=20):
    """
    Connects existing rooms using 'Guided Drunkard's Walk'.
    Picks two random floor tiles and digs a jagged path between them.
    """
    rows = len(input_grid)
    cols = len(input_grid[0])
    grid = [row[:] for row in input_grid] # Copy grid

    # Find all floor tiles so we can pick targets
    floors = []
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                floors.append((r, c))

    if not floors:
        return grid

    # Dig 'max_tunnels' number of connections
    for _ in range(max_tunnels):
        # 1. Pick two random points to connect
        start = random.choice(floors)
        end = random.choice(floors)
        
        # 2. Dig a "Biased Random Walk" from start to end
        current_r, current_c = start
        target_r, target_c = end
        
        while (current_r, current_c) != (target_r, target_c):
            # Calculate direction towards target
            move_r, move_c = 0, 0
            
            if current_r < target_r: move_r = 1
            elif current_r > target_r: move_r = -1
            
            if current_c < target_c: move_c = 1
            elif current_c > target_c: move_c = -1
            
            # 3. Add Noise (The "Wiggle")
            # 70% chance to move closer to target
            # 30% chance to move randomly (wiggle)
            if random.random() < 0.70:
                # Move along one axis towards goal
                if move_r != 0 and move_c != 0:
                    # Diagonal move? Pick one axis randomly
                    if random.random() < 0.5:
                        current_r += move_r
                    else:
                        current_c += move_c
                elif move_r != 0:
                    current_r += move_r
                elif move_c != 0:
                    current_c += move_c
            else:
                # Random stumble (Noise)
                directions = [(-1,0), (1,0), (0,-1), (0,1)]
                dr, dc = random.choice(directions)
                current_r += dr
                current_c += dc
                
            # Clamp to bounds (keep 1 tile border)
            current_r = max(1, min(rows-2, current_r))
            current_c = max(1, min(cols-2, current_c))
            
            # Carve
            grid[current_r][current_c] = 1

    return grid