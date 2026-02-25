from maze_generator.MazeConfig import MazeConfig
from maze_generator.Maze import Maze
from maze_generator.MazeConfigParser import MazeConfigParser
from pydantic import ValidationError
import random


class MazeGenerator:
    def __init__(self, config: MazeConfig):
        self.config = config
        self.maze = Maze(config)
        self._rng = random.Random(self.config.seed)

    def generate(self) -> Maze:
        start_x, start_y = self.config.entry
        visited_cells: set[tuple[int, int]] = set([(start_x, start_y)])
        frontier_walls: list[tuple[int, int, int, int, int]] = (
            self._get_adj_walls(start_x, start_y, visited_cells)
        )
        while frontier_walls:
            random_index = self._rng.randrange(len(frontier_walls))
            x1, y1, x2, y2, direction_bit = frontier_walls.pop(random_index)
            if (x2, y2) not in visited_cells:
                self.maze.break_wall(x1, y1, x2, y2, direction_bit)
                visited_cells.add((x2, y2))
                new_walls = self._get_adj_walls(x2, y2, visited_cells)
                frontier_walls.extend(new_walls)
        return self.maze

    def _get_adj_walls(
        self, x: int, y: int, visited_cells: set[tuple[int, int]]
    ) -> list[tuple[int, int, int, int, int]]:
        valid_walls = []
        directions = [
            (0, -1, Maze.NORTH),
            (1, 0, Maze.EAST),
            (0, 1, Maze.SOUTH),
            (-1, 0, Maze.WEST),
        ]

        for dx, dy, direction_bit in directions:
            nx, ny = x + dx, y + dy

            within_bounds: bool = (
                0 <= nx < self.maze.width and 0 <= ny < self.maze.height
            )
            if (
                within_bounds
                and (nx, ny) not in visited_cells
                and not self.maze.is_cell_in_42(nx, ny)
            ):
                valid_walls.append((x, y, nx, ny, direction_bit))

        return valid_walls


if __name__ == "__main__":
    try:
        maze_config = MazeConfigParser.load("config.txt")
        maze_generator = MazeGenerator(maze_config)
        maze_generator.generate()
    except OSError as err:
        print(err)
    except ValidationError as err:
        for error in err.errors():
            field = " -> ".join(map(str, error["loc"])).upper()
            msg: str = error.get("msg", "empty")
            input_val = error.get("input", "empty")
            print(
                f"MazeConfig error, Field {field} : "
                f"{msg} (received value : '{input_val}')"
            )
