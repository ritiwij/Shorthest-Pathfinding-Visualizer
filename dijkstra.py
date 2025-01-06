import pygame
import sys
import heapq
from tkinter import messagebox, Tk

# Initialize Pygame and set up the window
pygame.init()
window_width = 800
window_height = 800
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Dijkstra's Pathfinding Visualization")

# Frame rate controller
clock = pygame.time.Clock()

# Grid parameters
columns = 50
rows = 50
box_width = window_width // columns
box_height = window_height // rows

grid = []


# Box class for grid cells
class Box:
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.start = False
        self.wall = False
        self.target = False
        self.queued = False
        self.visited = False
        self.neighbours = []
        self.prior = None
        self.distance = float("inf")

    def draw(self, win, color):
        pygame.draw.rect(
            win,
            color,
            (self.x * box_width, self.y * box_height, box_width - 2, box_height - 2),
        )

    def set_neighbours(self):
        if self.x > 0:
            self.neighbours.append(grid[self.x - 1][self.y])
        if self.x < columns - 1:
            self.neighbours.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbours.append(grid[self.x][self.y + 1])

    def __lt__(self, other):
        return self.distance < other.distance


# Create the grid and set neighbors
for i in range(columns):
    arr = []
    for j in range(rows):
        arr.append(Box(i, j))
    grid.append(arr)

for i in range(columns):
    for j in range(rows):
        grid[i][j].set_neighbours()


def reconstruct_path(end_box):
    path = []
    current = end_box
    while current.prior:
        path.append(current)
        current = current.prior
    path.append(current)  # Include the start box
    return path[::-1]  # Reverse the path to go from start to end


def main():
    begin_search = False
    target_box_set = False
    searching = False
    path_found = False
    target_box = None
    start_box_set = False
    start_box = None
    queue = []
    needs_update = True
    path = []  # Initialize path as an empty list

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button click
                    x, y = pygame.mouse.get_pos()
                    i = x // box_width
                    j = y // box_height
                    if not start_box_set and not grid[i][j].wall:
                        start_box = grid[i][j]
                        start_box.start = True
                        start_box.distance = 0
                        heapq.heappush(queue, (start_box.distance, start_box))
                        start_box_set = True
                        needs_update = True
            elif event.type == pygame.MOUSEMOTION:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                i = x // box_width
                j = y // box_height
                # Draw Wall
                if event.buttons[0] and not grid[i][j].start and not grid[i][j].target:
                    grid[i][j].wall = True
                    needs_update = True
                # Set Target
                if event.buttons[2] and not target_box_set:
                    target_box = grid[i][j]
                    target_box.target = True
                    target_box_set = True
                    needs_update = True
            # Start Algorithm
            if event.type == pygame.KEYDOWN and target_box_set and start_box_set:
                begin_search = True
                searching = True

        if begin_search and searching and not path_found:
            if queue:
                current_distance, current_box = heapq.heappop(queue)

                if current_box == target_box:
                    searching = False
                    path_found = True
                    path = reconstruct_path(target_box)
                    needs_update = True
                else:
                    for neighbour in current_box.neighbours:
                        if not neighbour.wall and not neighbour.visited:
                            new_distance = (
                                current_box.distance + 1
                            )  # Assume uniform cost of 1
                            if new_distance < neighbour.distance:
                                neighbour.distance = new_distance
                                neighbour.prior = current_box
                                heapq.heappush(queue, (new_distance, neighbour))
                                neighbour.queued = True

                current_box.visited = True
                needs_update = True
            else:
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution", "There is no solution!")
                    searching = False
                    path_found = True

        if needs_update:
            window.fill((0, 0, 0))
            for i in range(columns):
                for j in range(rows):
                    box = grid[i][j]
                    color = (100, 100, 100)  # Default grey color
                    if box.queued:
                        color = (200, 0, 0)  # Red for queued cells
                    if box.visited:
                        color = (0, 200, 0)  # Green for visited cells
                    if box in path:
                        color = (0, 0, 200)  # Blue for the final path
                    if box.start:
                        color = (0, 200, 200)  # Cyan for the start point
                    if box.wall:
                        color = (10, 10, 10)  # Dark grey for walls
                    if box.target:
                        color = (200, 200, 0)  # Yellow for the target
                    box.draw(window, color)
            pygame.display.flip()
            needs_update = False

        clock.tick(30)  # Limits to 30 frames per second


if __name__ == "__main__":
    main()
