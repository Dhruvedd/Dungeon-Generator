import heapq

class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        
        self.g = 0  # Distance from start node
        self.h = 0  # Distance to end node (Heuristic)
        self.f = 0  # Total cost

    def __eq__(self, other):
        return self.position == other.position
    
    def __lt__(self, other):
        return self.f < other.f

def astar(maze, start, end):
    """
    Returns a list of tuples as a path from the given start to the given end in the given maze.
    maze: 2D array (0 for wall, 1 for floor)
    start: tuple (row, col)
    end: tuple (row, col)
    """
    
    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    heapq.heappush(open_list, start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[0]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            # Note: In your map 0 is Wall, 1 is Floor. 
            # If maze[r][c] == 0, it's a wall.
            if maze[node_position[0]][node_position[1]] == 0:
                continue

            new_node = Node(current_node, node_position)
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            if any(visited_child for visited_child in closed_list if visited_child == child):
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            # Heuristic: Manhattan distance
            child.h = abs(child.position[0] - end_node.position[0]) + abs(child.position[1] - end_node.position[1])
            child.f = child.g + child.h

            # Child is already in the open list
            if any(open_node for open_node in open_list if child == open_node and child.g > open_node.g):
                continue

            # Add the child to the open list
            heapq.heappush(open_list, child)
            
    return None # No path found