from Maze import Maze
from MazeConfigParser import MazeConfigParser
from pydantic import ValidationError
from MazeGenerator import MazeGenerator


class MazeRenderer:
    # On utilise le fond (Background) pour un rendu massif
    C_PATH = "\033[40m"  # Fond Noir
    C_WALL = "\033[47m"  # Fond Blanc
    C_ENTRY = "\033[45m"  # Fond Violet
    C_EXIT = "\033[41m"  # Fond Rouge
    RESET = "\033[0m"

    # Deux espaces créent un carré parfait dans la plupart des terminaux
    BLOCK = "  "

    @classmethod
    def display_terminal(cls, maze: Maze) -> None:
        # 1. Bordure supérieure complète
        print(f"{cls.C_WALL}{cls.BLOCK * (maze.width * 2 + 1)}{cls.RESET}")

        for y in range(maze.height):
            # ligne_cellules : contient [Mur Ouest][Cellule][Mur Est]...
            # ligne_murs : contient [Coin][Mur Sud][Coin]...
            line = f"{cls.C_WALL}{cls.BLOCK}"
            bottom_line = f"{cls.C_WALL}{cls.BLOCK}"

            for x in range(maze.width):
                # --- LA CELLULE ---
                # (Ici tu peux ajouter une logique pour l'entrée/sortie)
                cell_color = cls.C_PATH
                if (x, y) == maze.config.entry:
                    cell_color = cls.C_ENTRY
                elif (x, y) == maze.config.exit:
                    cell_color = cls.C_EXIT

                line += f"{cell_color}{cls.BLOCK}"

                # --- MUR EST ---
                if maze.has_wall(x, y, Maze.EAST):
                    line += f"{cls.C_WALL}{cls.BLOCK}"
                else:
                    line += f"{cls.C_PATH}{cls.BLOCK}"

                # --- MUR SUD ---
                if maze.has_wall(x, y, Maze.SOUTH):
                    bottom_line += f"{cls.C_WALL}{cls.BLOCK}"
                else:
                    bottom_line += f"{cls.C_PATH}{cls.BLOCK}"

                # --- LE COIN (toujours un mur sur cette image) ---
                bottom_line += f"{cls.C_WALL}{cls.BLOCK}"

            print(f"{line}{cls.RESET}")
            print(f"{bottom_line}{cls.RESET}")


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
        print("CONFIG PARSED: ", maze_config.__dict__)
        maze_generator = MazeGenerator(maze_config)
        maze = maze_generator.generate()
        display_maze_debug(maze)
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
