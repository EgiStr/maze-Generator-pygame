import random

def generate_maze(width, height):
    # Initialize the maze with walls
    maze = [[1 for _ in range(width)] for _ in range(height)]
    
    # Helper function to check if a cell is valid
    def is_valid(x, y):
        return 0 <= x < width and 0 <= y < height and maze[y][x] == 1

    def recursive_backtracking(x, y):
        # Mark the current cell as visited
        maze[y][x] = 0

        # Define the four possible directions (up, down, left, right)
        directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy

            if is_valid(new_x, new_y):
                # Remove the wall between the current cell and the next cell
                maze[y + dy // 2][x + dx // 2] = 0

                # Recursively visit the next cell
                recursive_backtracking(new_x, new_y)

    # Start the maze generation from a random cell
    start_x, start_y = random.randrange(0, width, 2), random.randrange(0, height, 2)
    recursive_backtracking(start_x, start_y)

    return maze

# Example usage:
width, height = 50, 50  # Adjust the size of the maze as needed
maze = generate_maze(width, height)

def is_valid(x, y):
    return 0 <= x < width and 0 <= y < height and maze[y][x] == 0


def get_neighbors(x, y):
    neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    return [(x, y) for x, y in neighbors if is_valid(x, y)]



def astar(maze, start, end):
    # Get the width and height of the maze
    width, height = len(maze[0]), len(maze)

    # Helper function to check if a cell is valid
    def is_valid(x, y):
        return 0 <= x < width and 0 <= y < height and maze[y][x] == 0

    # Helper function to get the neighbors of a cell
    def get_neighbors(x, y):
        neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        return [(x, y) for x, y in neighbors if is_valid(x, y)]

    # Initialize the starting cell as visited and push it into the queue
    queue, visited = [(start, [start])], set([start])

    # Loop until the queue is empty
    while queue:
        # Get the current cell and path
        (x, y), path = queue.pop(0)

        # Return the path if the current cell is the target cell
        # stringify 
        if (x, y) == end:
            return path
        
        # Check each neighbor of the current cell
        for neighbor in get_neighbors(x, y):
            # If the neighbor has not been visited yet
            if neighbor not in visited:
                # Mark it as visited and add it to the queue
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

# Example usage:
width, height = 30,30 # Adjust the size of the maze as needed
maze = generate_maze(width, height)
import random
start, end = (0, 0), (random.randrange(0, width), random.randrange(0, height))
path = astar(maze, start, end)

if path:
    print('Path found:')
    print(path)
# Print the path
    for y in range(height):
        for x in range(width):
            if (x, y) == start:
                print('S', end='')
            elif (x, y) == end:
                print('E', end='')
            elif (x, y) in path:
                print('O', end='')
            elif maze[y][x] == 1:
                print('#', end='')
            else:
                print(' ', end='')
        print()
else:
    print('Path not found!')