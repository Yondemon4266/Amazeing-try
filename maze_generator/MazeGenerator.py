from MazeConfig import MazeConfig
from MazeConfigParser import MazeConfigParser, MazeConfigError


class MazeGenerator:
    def __init__(self, config: MazeConfig):
        pass


if __name__ == "__main__":
    try:
        maze_config = MazeConfigParser.load("config.txt")
        print("CONFIG PARSED: ", maze_config.__dict__)

        maze = MazeGenerator(maze_config)
    except MazeConfigError as err:
        print(err.__class__.__name__, err)
