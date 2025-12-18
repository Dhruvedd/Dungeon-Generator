import time
import automata_generator
import miner
import search
import random

# Configuration matches your main.py
ROWS, COLS = 60, 80 # Based on 800x600 / 10

def run_benchmark(iterations=100):
    print(f"Benchmarking generation of {iterations} maps...")
    
    start_time = time.time()
    success_count = 0
    
    for i in range(iterations):
        # 1. Generate Base
        base_grid = automata_generator.generate_cave(ROWS, COLS, iterations=2, fill_percent=0.80)
        
        # 2. Connect
        connected_grid = miner.mine_tunnels(base_grid)
        
        # 3. Smooth
        final_grid = automata_generator.generate_cave(ROWS, COLS, iterations=2, input_grid=connected_grid)
        
        # 4. cleanup '2's
        grid_map = []
        for r in range(ROWS):
            row = []
            for c in range(COLS):
                val = 1 if final_grid[r][c] == 2 else final_grid[r][c]
                row.append(val)
            grid_map.append(row)
            
        # 5. Verify (Search)
        # Find valid start/end
        floors = [(r, c) for r in range(ROWS) for c in range(COLS) if grid_map[r][c] == 1]
        if len(floors) > 2:
            start = floors[0]
            end = floors[-1]
            path = search.astar(grid_map, start, end)
            if path:
                success_count += 1

    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / iterations

    print(f"\n--- RESULTS ---")
    print(f"Total Time: {total_time:.4f} seconds")
    print(f"Average Time per Map: {avg_time:.4f} seconds ({avg_time*1000:.2f} ms)")
    print(f"Solvability Rate: {success_count}/{iterations} ({success_count/iterations*100}%)")

if __name__ == "__main__":
    run_benchmark()