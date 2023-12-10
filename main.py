import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

class GameSelector(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Game Selector")
        self.geometry("300x150")

        self.label = tk.Label(self, text="Choose a game:")
        self.label.pack(pady=10)

        self.maze_button = tk.Button(self, text="Maze Solving", command=self.run_maze_solver)
        self.maze_button.pack(pady=10)

        self.tic_tac_toe_button = tk.Button(self, text="Tic-tac-toe", command=self.run_tic_tac_toe)
        self.tic_tac_toe_button.pack(pady=10)

    def run_maze_solver(self):
        try:
            subprocess.run([sys.executable, "maze.py"])
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def run_tic_tac_toe(self):
        try:
            subprocess.run([sys.executable, "tictactoe.py"])
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    app = GameSelector()
    app.mainloop()
