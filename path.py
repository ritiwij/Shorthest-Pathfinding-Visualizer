from tkinter import messagebox, Tk
import pygame
import sys
import heapq

# priority queue


window_width = 800
window_height = 800

window = pygame.display.set_mode((window_width, window_height))

columns = 50
rows = 50

box_width = window_width // columns
box_height = window_height // rows

grid = []
queue = []
path = []


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
        self.distance = float("inf")  # Initialize distance with infinity

    # we have draw the window
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


# Create Grid
for i in range(columns):
    arr = []
    for j in range(rows):
        arr.append(Box(i, j))
    grid.append(arr)

# Set Neighbours
for i in range(columns):
    for j in range(rows):
        grid[i][j].set_neighbours()

# start_box = grid[0][0]
# start_box.start = True
# start_box.visited = True
# queue.append(start_box)


# NORMAL BFS SEARCH

"""

def main():
    begin_search = False
    target_box_set = False
    searching = True
    target_box = None
    start_box_set = False
    

    while True:
        for event in pygame.event.get():
            # Quit Window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Mouse Controls
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button click
                    x, y = pygame.mouse.get_pos()
                    i = x // box_width
                    j = y // box_height
                    if not start_box_set and not grid[i][j].wall:
                        start_box = grid[i][j]
                        start_box.start = True
                        start_box.visited = True
                        queue.append(start_box)
                        start_box_set = True

            # Motion of mouse is saved here
            elif event.type == pygame.MOUSEMOTION:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                # Draw Wall
                if event.buttons[0]:
                    i = x // box_width
                    j = y // box_height
                    grid[i][j].wall = True
                # Set Target
                if event.buttons[2] and not target_box_set:
                    i = x // box_width
                    j = y // box_height
                    target_box = grid[i][j]
                    target_box.target = True
                    target_box_set = True
            # Start Algorithm
            if event.type == pygame.KEYDOWN and target_box_set:
                begin_search = True
                #  This condition checks if the event is a key press. When the user presses any key on the keyboard, a pygame.KEYDOWN event is generated.

        if begin_search:
            if len(queue) > 0 and searching:
                current_box = queue.pop(0)
                current_box.visited = True
                if current_box == target_box:
                    searching = False
                    while current_box.prior != start_box:
                        path.append(current_box.prior)
                        current_box = current_box.prior
                else:
                    for neighbour in current_box.neighbours:
                        if not neighbour.queued and not neighbour.wall:
                            neighbour.queued = True
                            neighbour.prior = current_box
                            queue.append(neighbour)
            else:
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution", "There is no solution!")
                    searching = False

        window.fill((0, 0, 0))

        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                box.draw(window, (100, 100, 100))

                if box.queued:
                    box.draw(window, (200, 0, 0))
                if box.visited:
                    box.draw(window, (0, 200, 0))
                if box in path:
                    box.draw(window, (0, 0, 200))

                if box.start:
                    box.draw(window, (0, 200, 200))
                if box.wall:
                    box.draw(window, (10, 10, 10))
                if box.target:
                    box.draw(window, (200, 200, 0))

        pygame.display.flip()


main()

"""

# Djikstra Algorithm


def main():
    begin_search = False
    target_box_set = False
    searching = True
    target_box = None
    start_box_set = False
    start_box = None
    queue = []  # Priority queue

    while True:
        for event in pygame.event.get():
            # Quit Window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Mouse Controls
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button click
                    x, y = pygame.mouse.get_pos()
                    i = x // box_width
                    j = y // box_height
                    if not start_box_set and not grid[i][j].wall:
                        start_box = grid[i][j]
                        start_box.start = True
                        # start_box.visited = True
                        start_box.distance = 0
                        heapq.heappush(queue, (start_box.distance, start_box))
                        start_box_set = True

            elif event.type == pygame.MOUSEMOTION:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                # Draw Wall
                if event.buttons[0]:
                    i = x // box_width
                    j = y // box_height
                    grid[i][j].wall = True
                # Set Target
                if event.buttons[2] and not target_box_set:
                    i = x // box_width
                    j = y // box_height
                    target_box = grid[i][j]
                    target_box.target = True
                    target_box_set = True
            # Start Algorithm
            if event.type == pygame.KEYDOWN and target_box_set:
                begin_search = True

        if begin_search:
            if len(queue) > 0 and searching:
                current_distance, current_box = heapq.heappop(queue)
                if current_box.visited:
                    continue
                current_box.visited = True

                if current_box == target_box:
                    searching = False
                    while current_box.prior != start_box:
                        path.append(current_box.prior)
                        current_box = current_box.prior
                else:
                    for neighbour in current_box.neighbours:
                        if not neighbour.wall:
                            new_distance = (
                                current_distance + 1
                            )  # Assuming uniform cost for each step
                            if new_distance < neighbour.distance:
                                neighbour.distance = new_distance
                                neighbour.prior = current_box
                                heapq.heappush(queue, (neighbour.distance, neighbour))
            else:
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution", "There is no solution!")
                    searching = False

        window.fill((0, 0, 0))

        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                box.draw(window, (100, 100, 100))

                if box.queued:
                    box.draw(window, (200, 0, 0))
                if box.visited:
                    box.draw(window, (0, 200, 0))
                if box in path:
                    box.draw(window, (0, 0, 200))

                if box.start:
                    box.draw(window, (0, 200, 200))
                if box.wall:
                    box.draw(window, (10, 10, 10))
                if box.target:
                    box.draw(window, (200, 200, 0))

        pygame.display.flip()


main()
