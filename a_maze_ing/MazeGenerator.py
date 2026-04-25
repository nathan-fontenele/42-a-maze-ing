from typing import List, Dict, Tuple, Union
from random import randint, seed, choice, shuffle
from sys import setrecursionlimit
from time import sleep
from os import system

from a_maze_ing.Parser import Parsing
from a_maze_ing.Cell import Cell
from a_maze_ing.Colors import WHITE, MAGENTA, CYAN

OPPOSITES: Dict[str, str] = {"N": "S", "E": "W", "S": "N", "W": "E"}
WALL_BITS: Dict[str, int] = {"N": 0, "E": 1, "S": 2, "W": 3}


class MazeGenerator:
    """Generates, solves, and renders a maze."""
    def __init__(
        self,
        config_file: str,
        animation: bool
    ) -> None:
        """Initialize the maze generator from a config file."""
        setrecursionlimit(10000)
        p: Parsing = Parsing(config_file)
        p.set_config()
        self.WIDTH: int = p.WIDTH
        self.HEIGHT: int = p.HEIGHT
        self.ANIMATION: bool = animation

        self.maze: List[List[Cell]] = []
        if p.SEED is None:
            self.seed: int = randint(0, 99999999)
        else:
            self.seed = p.SEED
        self.OUTPUT_FILE: str = p.OUTPUT_FILE
        self.PERFECT: Union[None, bool] = p.PERFECT
        self.ENTRY: Dict[str, int] = p.ENTRY
        self.EXIT: Dict[str, int] = p.EXIT
        self.solutions: List[List[str]] = []
        seed(self.seed)
        self.maze_init()

    def maze_init(self) -> None:
        """Initialize the grid and stamp the '42' pattern as static cells."""
        for y in range(self.HEIGHT):
            row: List = []
            for x in range(self.WIDTH):
                cell: Cell = Cell(15, False, False)
                row.append(cell)
            self.maze.append(row)

        offset_x: int = (self.WIDTH - 7) // 2
        offset_y: int = (self.HEIGHT - 5) // 2

        if self.WIDTH >= 7 and self.HEIGHT >= 5:
            pattern_42: List[Tuple[int, int]] = [
                (0, 0), (0, 1), (0, 2), (1, 2), (2, 0),
                (2, 1), (2, 2), (2, 3), (2, 4),  # '4'

                (4, 0), (5, 0), (6, 0), (6, 1), (6, 2), (5, 2),
                (4, 2), (4, 3), (4, 4), (5, 4), (6, 4)  # '2'
            ]

            for rel_x, rel_y in pattern_42:
                tx, ty = offset_x + rel_x, offset_y + rel_y

                if (
                    (self.ENTRY['x'] == tx and self.ENTRY['y'] == ty) or
                    (self.EXIT['x'] == tx and self.EXIT['y'] == ty)
                ):
                    print("Entry & Exit must not be in 42 position")
                    exit(0)

                self.maze[ty][tx].walls = 15
                self.maze[ty][tx].static = True
                self.maze[ty][tx].visited = True
        else:
            print("Error: Maze size too small for '42' pattern.")
            exit(0)

    def render_frame(
        self,
        maze_color: str = WHITE,
        save: bool = False,
        wall_style: str = "█"
    ) -> str:
        """Render the current maze frame to the terminal or return as string."""
        wall_char: str = wall_style
        BULLET_COLOR: str = MAGENTA
        rendered: str = ""

        if save:
            rendered = "========== RENDERED MAZE ==========\n"
            rendered += f"Entry Coordinates: {self.ENTRY}\n"
            rendered += f"Exit Coordinates: {self.EXIT}\n"
            rendered += f"Solution: {self.shortest()}\n"
            rendered += "===================================\n\n"
            BULLET_COLOR = ""
            maze_color = ""
        else:
            system('clear')

        for y in range(len(self.maze)):
            row = self.maze[y]
            left: str = ""
            right: str = ""
            line1: str = ""
            line2: str = ""

            for x in range(len(row)):
                cell: Cell = row[x]

                if x == self.ENTRY['x'] and y == self.ENTRY['y']:
                    cell_representation = f"{BULLET_COLOR} ● {maze_color}"
                elif x == self.EXIT['x'] and y == self.EXIT['y']:
                    cell_representation = f"{BULLET_COLOR} ● {maze_color}"
                else:
                    cell_representation = "   "

                if cell.walls & 1:
                    line1 += f"{wall_char}{wall_char}{wall_char}{wall_char}{wall_char}"
                else:
                    line1 += f"{wall_char}   {wall_char}"

                left = wall_char if cell.walls & 8 else " "
                right = wall_char if cell.walls & 2 else " "

                if cell.walls == 15:
                    line2 += f"{wall_char}{wall_char}{wall_char}{wall_char}{wall_char}"
                else:
                    line2 += f"{left}{cell_representation}{right}"

            if save:
                rendered += f"{line1}\n"
                rendered += f"{line2}\n"
            else:
                print(f"{maze_color}{line1}")
                print(f"{maze_color}{line2}")

        if save:
            rendered += f"{wall_char}{wall_char}{wall_char}{wall_char}{wall_char}" * len(self.maze[0])
            return f"{rendered}\n\n"
        else:
            print(f"{maze_color}{wall_char}{wall_char}{wall_char}{wall_char}{wall_char}" * len(self.maze[0]))
            if self.ANIMATION:
                sleep(.03)
            return ""

    def save_rendered(self) -> None:
        """Export the rendered ASCII maze to a file."""
        try:
            with open(f"rendered_{self.OUTPUT_FILE}", "w") as output:
                output.write(self.render_frame(save=True))
                print(f"[+] Maze saved to: rendered_{self.OUTPUT_FILE}")

        except Exception as e:
            print(f"[!] Unable to save your maze: {e}")

    def shortest(self) -> str:
        """Return the shortest solution path as a direction string."""
        try:
            best: List[str] = self.solutions[0]
            for path in self.solutions:
                if len(path) < len(best):
                    best = path
            return "".join(best)
        except IndexError:
            return ""

    def display_solution(
        self,
        maze_color: str = WHITE,
        custom_solution: str = " ● "
    ) -> None:
        """Animate and display the shortest solution path on the maze."""
        if not len(self.solutions):
            self.render_frame()
            print("\n[!] No maze to find solutions!")
            return

        path: str = self.shortest()
        solution_cells: List = []
        current: List = [self.ENTRY['x'], self.ENTRY['y']]

        for direction in path:
            if direction == 'N':
                current = [current[0], current[1] - 1]
            if direction == 'E':
                current = [current[0] + 1, current[1]]
            if direction == 'S':
                current = [current[0], current[1] + 1]
            if direction == 'W':
                current = [current[0] - 1, current[1]]

            solution_cells.append(current)

            system('clear')
            for y in range(len(self.maze)):
                row = self.maze[y]
                line1 = ""
                line2 = ""
                cell_representation: str = ""

                for x in range(len(row)):
                    cell = row[x]

                    if (
                        ([x, y] in solution_cells)
                        and not (x == self.ENTRY['x'] and y == self.ENTRY['y'])
                        and not (x == self.EXIT['x'] and y == self.EXIT['y'])
                    ):
                        cell_representation = f"{CYAN}{custom_solution}{maze_color}"
                    elif x == self.ENTRY['x'] and y == self.ENTRY['y']:
                        cell_representation = f"{MAGENTA} ● {maze_color}"
                    elif x == self.EXIT['x'] and y == self.EXIT['y']:
                        cell_representation = f"{MAGENTA} ● {maze_color}"
                    else:
                        cell_representation = "   "

                    if cell.walls & 1:
                        line1 += "█████"
                    else:
                        line1 += "█   █"

                    left = "█" if cell.walls & 8 else " "
                    right = "█" if cell.walls & 2 else " "

                    if cell.walls == 15:
                        line2 += "█████"
                    else:
                        line2 += f"{left}{cell_representation}{right}"

                print(f"{maze_color}{line1}")
                print(f"{maze_color}{line2}")

            print(f"{maze_color}█████" * len(self.maze[0]))
            if self.ANIMATION:
                sleep(.1)

    def get_maze_str(self) -> str:
        """Serialize the maze walls to a hex string."""
        output: str = ""
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                val: int = self.maze[y][x].walls
                output += f"{val:X}"
            output += "\n"
        return output

    def save_maze(self) -> None:
        """Save the maze in hex format with entry, exit, and solution."""
        with open(self.OUTPUT_FILE, "w") as f:
            f.write(self.get_maze_str())
            f.write(f"\n{self.ENTRY['x']},{self.ENTRY['y']}")
            f.write(f"\n{self.EXIT['x']},{self.EXIT['y']}\n")
            f.write("".join(self.shortest()))

    def open_wall(self, cell: Cell, direction: str) -> None:
        """Remove the wall in the given direction from a cell."""
        cell.walls &= ~(1 << WALL_BITS[direction])

    def dfs_generate(self) -> None:
        """Start DFS maze generation from a seed-derived position."""
        x: int = self.seed % self.WIDTH
        y: int = self.seed % self.HEIGHT
        while self.maze[y][x].static:
            x = (self.seed * 10) % self.WIDTH
            y = (self.seed * 10) % self.HEIGHT

        self.make_maze(x, y)
        if not self.PERFECT:
            self.create_multiple_paths()

    def make_maze(self, x: int, y: int) -> None:
        """Recursively carve passages using DFS."""
        self.render_frame(maze_color=WHITE)
        neighbors: List = []
        self.maze[y][x].visited = True

        if y - 1 >= 0 and not self.maze[y - 1][x].visited:
            neighbors.append((x, y - 1, "N"))
        if x + 1 < self.WIDTH and not self.maze[y][x + 1].visited:
            neighbors.append((x + 1, y, "E"))
        if y + 1 < self.HEIGHT and not self.maze[y + 1][x].visited:
            neighbors.append((x, y + 1, "S"))
        if x - 1 >= 0 and not self.maze[y][x - 1].visited:
            neighbors.append((x - 1, y, "W"))

        shuffle(neighbors)
        for tx, ty, direction in neighbors:
            if not self.maze[ty][tx].visited:
                self.open_wall(self.maze[y][x], direction)
                self.open_wall(self.maze[ty][tx], OPPOSITES[direction])
                self.make_maze(tx, ty)

    def reset_maze_visited(self) -> None:
        """Reset the visited flag on every cell."""
        for row in self.maze:
            for cell in row:
                cell.visited = False

    def start_solving(self) -> None:
        """Launch the recursive solver from entry to exit."""
        self.solve_maze(
            self.ENTRY['x'],
            self.ENTRY['y'],
            self.EXIT['x'],
            self.EXIT['y'],
            []
        )

    def solve_maze(
        self,
        x: int,
        y: int,
        sx: int,
        sy: int,
        solve: List
    ) -> None:
        """Recursively find all paths from (x, y) to (sx, sy)."""
        if x == sx and y == sy:
            self.solutions.append(list(solve))
            return

        neighbors: List = []
        self.maze[y][x].visited = True

        if y - 1 >= 0 and (self.maze[y][x].walls & (1 << 0)) == 0:
            neighbors.append((x, y - 1, "N"))
        if x + 1 < self.WIDTH and (self.maze[y][x].walls & (1 << 1)) == 0:
            neighbors.append((x + 1, y, "E"))
        if y + 1 < self.HEIGHT and (self.maze[y][x].walls & (1 << 2)) == 0:
            neighbors.append((x, y + 1, "S"))
        if x - 1 >= 0 and (self.maze[y][x].walls & (1 << 3)) == 0:
            neighbors.append((x - 1, y, "W"))

        for tx, ty, direction in neighbors:
            if not self.maze[ty][tx].static and not self.maze[ty][tx].visited:
                solve.append(direction)
                self.solve_maze(tx, ty, sx, sy, solve)
                solve.pop()
        self.maze[y][x].visited = False

    def create_multiple_paths(self) -> None:
        """Break additional walls to create a non-perfect (looping) maze."""
        x: int = 0
        y: int = 0
        candidates: List = []
        for row in self.maze:
            x = 0
            for cell in row:
                if randint(0, 9) < 1 and not cell.static:
                    if y - 1 >= 0 and not self.maze[y - 1][x].static:
                        candidates.append((x, y - 1, "N"))
                    if x + 1 < self.WIDTH and not self.maze[y][x + 1].static:
                        candidates.append((x + 1, y, "E"))
                    if y + 1 < self.HEIGHT and not self.maze[y + 1][x].static:
                        candidates.append((x, y + 1, "S"))
                    if x - 1 >= 0 and not self.maze[y][x - 1].static:
                        candidates.append((x - 1, y, "W"))
                    selected = choice(candidates)
                    self.open_wall(cell, selected[2])
                    self.open_wall(
                        self.maze[selected[1]][selected[0]],
                        OPPOSITES[selected[2]]
                    )
                    candidates.clear()
                x += 1
            y += 1
        self.render_frame(maze_color=WHITE)

    def bfs_generate(self) -> None:
        """Start BFS maze generation from a seed-derived position."""
        x: int = self.seed % self.WIDTH
        y: int = self.seed % self.HEIGHT
        while self.maze[y][x].static:
            x = (self.seed * 10) % self.WIDTH
            y = (self.seed * 10) % self.HEIGHT

        self.bfs_make_maze(x, y)
        self.render_frame(maze_color=WHITE)
        if not self.PERFECT:
            self.create_multiple_paths()

    def bfs_make_maze(self, x: int, y: int) -> None:
        """Iteratively carve passages using BFS."""
        self.maze[y][x].visited = True
        queue: List = []
        queue.insert(0, (self.maze[y][x], y, x))
        while queue:
            neighbors: List = []
            y = queue[0][1]
            x = queue[0][2]
            queue.pop(0)

            if y - 1 >= 0 and not self.maze[y - 1][x].visited:
                neighbors.append((x, y - 1, "N"))
            if x + 1 < self.WIDTH and not self.maze[y][x + 1].visited:
                neighbors.append((x + 1, y, "E"))
            if y + 1 < self.HEIGHT and not self.maze[y + 1][x].visited:
                neighbors.append((x, y + 1, "S"))
            if x - 1 >= 0 and not self.maze[y][x - 1].visited:
                neighbors.append((x - 1, y, "W"))

            shuffle(neighbors)

            for tx, ty, direction in neighbors:
                if not self.maze[ty][tx].visited:
                    self.open_wall(self.maze[y][x], direction)
                    self.open_wall(self.maze[ty][tx], OPPOSITES[direction])
                    self.maze[ty][tx].visited = True
                    queue.insert(0, (self.maze[ty][tx], ty, tx))
                    self.render_frame(maze_color=WHITE)
