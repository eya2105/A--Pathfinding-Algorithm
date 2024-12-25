import pygame
import math
from queue import PriorityQueue

# Set up window dimensions
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

# Define colors
PURPLE = (138, 43, 226)    # Purple for start and end points
LIGHT_BLUE = (173, 216, 230) # Light Blue for grid lines
DARK_BLUE = (0, 0, 139)    # Dark Blue for obstacles
YELLOW = (255, 255, 0)     # Yellow for visited cells
WHITE = (255, 255, 255)    # White for empty cells
BLACK = (0, 0, 0)          # Black for text and borders
GREEN = (34, 139, 34)      # Green for open cells
TURQUOISE = (64, 224, 208) # Turquoise for the end point
RED = (255, 99, 71)        # Red for path cells

# Cell class represents each cell in the grid
class Cell:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE  # Default color for empty cells
        self.neighbors = [] # List of neighboring cells
        self.width = width
        self.total_rows = total_rows

    def get_position(self):
        return self.row, self.col

    def is_visited(self):
        return self.color == YELLOW

    def is_open(self):
        return self.color == GREEN

    def is_obstacle(self):
        return self.color == DARK_BLUE

    def is_start(self):
        return self.color == PURPLE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE  # Reset cell to empty

    def set_start(self):
        self.color = PURPLE  # Set cell as start point

    def set_visited(self):
        self.color = YELLOW  # Set cell as visited

    def set_open(self):
        self.color = GREEN  # Set cell as open (in the open set)

    def set_obstacle(self):
        self.color = DARK_BLUE  # Set cell as obstacle

    def set_end(self):
        self.color = TURQUOISE  # Set cell as end point

    def set_path(self):
        self.color = PURPLE  # Set cell as part of the path

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    # Update neighbors for the current cell (adjacent cells that are not obstacles)
    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_obstacle(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_obstacle(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_obstacle(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_obstacle(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


# Heuristic function for A* (Manhattan distance by default)
def heuristic(cell1, cell2, mode="manhattan"):
    x1, y1 = cell1
    x2, y2 = cell2
    if mode == "manhattan":
        return abs(x1 - x2) + abs(y1 - y2)  # Manhattan distance
    elif mode == "euclidean":
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)  # Euclidean distance


# Reconstruct the path from the end cell to the start cell
def reconstruct_path(came_from, current_cell, draw):
    while current_cell in came_from:
        current_cell = came_from[current_cell]
        current_cell.set_path()  # Mark the path
        draw()  # Redraw the grid


# A* algorithm implementation
def a_star_algorithm(draw, grid, start_cell, end_cell):
    count = 0
    open_set = PriorityQueue()  # Priority queue for open set
    open_set.put((0, count, start_cell))  # Start with the start cell
    came_from = {}  # Dictionary to track the path
    g_score = {cell: float("inf") for row in grid for cell in row}  # g-score for each cell
    g_score[start_cell] = 0
    f_score = {cell: float("inf") for row in grid for cell in row}  # f-score for each cell
    f_score[start_cell] = heuristic(start_cell.get_position(), end_cell.get_position())  # Heuristic for start cell

    open_set_hash = {start_cell}  # Set for quick lookup of open set cells

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current_cell = open_set.get()[2]  # Get the cell with the lowest f-score
        open_set_hash.remove(current_cell)

        if current_cell == end_cell:  # If we reached the end cell
            reconstruct_path(came_from, end_cell, draw)
            end_cell.set_end()  # Mark the end cell
            return True

        for neighbor in current_cell.neighbors:
            temp_g_score = g_score[current_cell] + 1  # Calculate g-score for neighbor

            if temp_g_score < g_score[neighbor]:  # If this path is better
                came_from[neighbor] = current_cell  # Update the path
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_position(), end_cell.get_position())  # Update f-score
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))  # Add to open set
                    open_set_hash.add(neighbor)
                    neighbor.set_open()  # Mark the neighbor as open

        draw()  # Redraw the grid

        if current_cell != start_cell:
            current_cell.set_visited()  # Mark the current cell as visited

    return False


# Create a grid of cells
def create_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            cell = Cell(i, j, gap, rows)
            grid[i].append(cell)

    return grid


# Draw the grid lines
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, LIGHT_BLUE, (0, i * gap), (width, i * gap))  # Horizontal lines
        for j in range(rows):
            pygame.draw.line(win, LIGHT_BLUE, (j * gap, 0), (j * gap, width))  # Vertical lines


# Draw all cells and grid lines
def draw(win, grid, rows, width):
    win.fill(WHITE)  # Fill the window with white

    for row in grid:
        for cell in row:
            cell.draw(win)  # Draw each cell

    draw_grid(win, rows, width)  # Draw the grid lines
    pygame.display.update()  # Update the display


# Get the row and column of the clicked position
def get_clicked_position(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


# Main function to run the program
def main(win, width):
    ROWS = 50  # Number of rows and columns in the grid
    grid = create_grid(ROWS, width)  # Create the grid

    start_cell = None
    end_cell = None

    run = True
    while run:
        draw(win, grid, ROWS, width)  # Draw the grid and cells
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Handle mouse clicks to set start, end, and obstacle cells
            if pygame.mouse.get_pressed()[0]: # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, ROWS, width)
                cell = grid[row][col]
                if not start_cell and cell != end_cell:
                    start_cell = cell
                    start_cell.set_start()  # Set the start point

                elif not end_cell and cell != start_cell:
                    end_cell = cell
                    end_cell.set_end()  # Set the end point

                elif cell != end_cell and cell != start_cell:
                    cell.set_obstacle()  # Set obstacle

            # Handle right-click to reset cells
            elif pygame.mouse.get_pressed()[2]: # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, ROWS, width)
                cell = grid[row][col]
                cell.reset()  # Reset the cell
                if cell == start_cell:
                    start_cell = None
                elif cell == end_cell:
                    end_cell = None

            # Run the A* algorithm when space is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start_cell and end_cell:
                    for row in grid:
                        for cell in row:
                            cell.update_neighbors(grid)  # Update neighbors

                    a_star_algorithm(lambda: draw(win, grid, ROWS, width), grid, start_cell, end_cell)  # Run A* algorithm

                # Clear the grid when 'C' is pressed
                if event.key == pygame.K_c:
                    start_cell = None
                    end_cell = None
                    grid = create_grid(ROWS, width)  # Reset the grid

    pygame.quit()  # Quit pygame when done


# Run the main function
main(WIN, WIDTH)
