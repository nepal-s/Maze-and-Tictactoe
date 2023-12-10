import sys
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import heapq

class Node():
    def __init__(self, state, parent, action, cost=0, heuristic=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.heuristic = heuristic

    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

class PriorityQueueFrontier(StackFrontier):
    def __init__(self):
        self.frontier = []

    def add(self, node):
        heapq.heappush(self.frontier, node)

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            return heapq.heappop(self.frontier)

class Maze():
    def __init__(self, filename):
        with open(filename) as f:
            contents = f.read()

        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")

        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None

    def display(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()

    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result

    def solve(self):
        self.num_explored = 0
        start = Node(state=self.start, parent=None, action=None)
        frontier = StackFrontier()
        frontier.add(start)
        self.explored = set()

        while True:
            if frontier.empty():
                raise Exception("no solution")

            node = frontier.remove()
            self.num_explored += 1

            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            self.explored.add(node.state)

            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)

    def manhattan_distance(self, state):
        return abs(state[0] - self.goal[0]) + abs(state[1] - self.goal[1])

    def a_star_solve(self):
        self.num_explored = 0
        start = Node(state=self.start, parent=None, action=None, cost=0, heuristic=self.manhattan_distance(self.start))
        frontier = PriorityQueueFrontier()
        frontier.add(start)
        self.explored = set()

        while True:
            if frontier.empty():
                raise Exception("no solution")

            node = frontier.remove()
            self.num_explored += 1

            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            self.explored.add(node.state)

            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    cost = node.cost + 1
                    heuristic = self.manhattan_distance(state)
                    child = Node(state=state, parent=node, action=action, cost=cost, heuristic=heuristic)
                    frontier.add(child)

    def output_image(self, filename, show_solution=True, show_explored=False):
        cell_size = 50
        cell_border = 2

        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),  # Removed the extra width for the text area
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    fill = (40, 40, 40)
                elif (i, j) == self.start:
                    fill = (255, 0, 0)
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)
                else:
                    fill = (237, 240, 252)

                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)

class MazeSolverGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Maze Solver")
        self.geometry("400x200")

        self.label = tk.Label(self, text="Choose an option:")
        self.label.pack(pady=10)

        self.default_button = tk.Button(self, text="Default", command=self.solve_default)
        self.default_button.pack(pady=10)

        self.upload_button = tk.Button(self, text="Upload", command=self.solve_upload)
        self.upload_button.pack(pady=10)

    def solve_default(self):
        maze_file = "maze2.txt"
        self.solve_maze(maze_file)

    def solve_upload(self):
        maze_file = filedialog.askopenfilename(title="Select Maze File", filetypes=[("Text files", "*.txt")])
        if maze_file:
            self.solve_maze(maze_file)

    def solve_maze(self, maze_file):
        try:
            # DFS
            m_dfs = Maze(maze_file)
            print("DFS:")
            m_dfs.display()
            print("Solving with DFS...")
            m_dfs.solve()
            print("States Explored:", m_dfs.num_explored)
            print("Solution:")
            m_dfs.display()
            m_dfs.output_image("maze_dfs.png", show_explored=True)
            # Show the DFS solution image
            img_dfs = Image.open("maze_dfs.png")
            plt.imshow(img_dfs)
            plt.title("Pathfinding using DFS")
            plt.axis('off')  # Turn off axis values
            plt.show()

            # A* with Manhattan Distance Heuristic
            m_astar = Maze(maze_file)
            print("\nA* with Manhattan Distance Heuristic:")
            m_astar.display()
            print("Solving with A*...")
            m_astar.a_star_solve()
            print("States Explored:", m_astar.num_explored)
            print("Solution:")
            m_astar.display()
            m_astar.output_image("maze_astar.png", show_explored=True)
            # Show the A* solution image
            img_astar = Image.open("maze_astar.png")
            plt.imshow(img_astar)
            plt.title("Pathfinding using A*")
            plt.axis('off')  # Turn off axis values
            plt.show()

        except Exception as e:
            print(f"Error: {e}")
            # Handle the exception as needed

if __name__ == "__main__":
    app = MazeSolverGUI()
    app.mainloop()
