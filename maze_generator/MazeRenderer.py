from Maze import Maze
from MazeConfigParser import MazeConfigParser
from pydantic import ValidationError
from MazeGenerator import MazeGenerator


class MazeRenderer:
    NORTH = 1  # 0001
    EAST = 2  # 0010
    SOUTH = 4  # 0100
    WEST = 8  # 1000

    @classmethod
    def display_terminal(cls, maze: Maze) -> None:
        for y in range(maze.height):
            line_north = ""
            line_west = ""
            for x in range(maze.width):
                cell_index: int = maze.grid[maze.get_index(x, y)]
                if cell_index & cls.NORTH:
                    line_north += "---"
                else:
                    line_north += " "
                if cell_index & cls.WEST:
                    line_west += "|"
                else:
                    line_west += " "
            print(line_north + "+")
            print(line_west + "|")


if __name__ == "__main__":
    try:
        maze_config = MazeConfigParser.load("config.txt")
        print("CONFIG PARSED: ", maze_config.__dict__)

        maze_generator = MazeGenerator(maze_config)
        maze = maze_generator.generate()
        MazeRenderer.display_terminal(maze)
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
