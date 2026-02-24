from Maze import Maze
from MazeConfigParser import MazeConfigParser
from pydantic import ValidationError
from MazeGenerator import MazeGenerator


class MazeRenderer:

    @classmethod
    def display_terminal(cls, maze: Maze, show_path: bool = False) -> None:
        # Couleurs basées sur votre dictionnaire config1
        WALL = "\033[47m  \033[0m"  # Fond Blanc (2 espaces)
        # PATH = "\033[44m  \033[0m"  # Fond Bleu pour le chemin
        EMPTY = "\033[40m  \033[0m"  # Fond Noir
        ENTRY = "\033[45m  \033[0m"  # Fond Violet
        EXIT = "\033[41m  \033[0m"  # Fond Rouge

        # 1. On dessine d'abord le mur supérieur (North)
        print(WALL * (maze.width * 2 + 1))

        for y in range(maze.height):
            # Ligne de contenu de la cellule
            line = WALL  # Mur Ouest de la bordure
            for x in range(maze.width):
                # Déterminer la couleur du centre de la cellule
                if (x, y) == maze.config.entry:
                    line += ENTRY
                elif (x, y) == maze.config.exit:
                    line += EXIT
                elif maze.is_cell_in_42(x, y):
                    line += "\033[43m42\033[0m"
                else:
                    line += EMPTY

                # Mur Est de la cellule
                if maze.has_wall(x, y, Maze.EAST):
                    line += WALL
                else:
                    line += EMPTY
            print(line)

            # Ligne des murs Sud
            south_line = WALL
            for x in range(maze.width):
                if maze.has_wall(x, y, Maze.SOUTH):
                    south_line += WALL + WALL  # Le mur et le coin
                else:
                    south_line += EMPTY + WALL  # Vide et le coin
            print(south_line)


def display_maze_debug(maze: Maze) -> None:
    for y in range(maze.height):
        line: str = ""
        for x in range(maze.width):
            index: int = maze.get_index(x, y)
            val: int = maze.grid[index]
            # :X converts in hexa CAPS
            line += f"{val:X}"
        print(line)


if __name__ == "__main__":
    try:
        maze_config = MazeConfigParser.load("config.txt")
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
