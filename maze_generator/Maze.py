from MazeConfig import MazeConfig


class Maze:
    NORTH = 1  # 0001
    EAST = 2  # 0010
    SOUTH = 4  # 0100
    WEST = 8  # 1000

    OPPOSITE = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}

    def __init__(self, config: MazeConfig) -> None:
        self.config: MazeConfig = config
        self.width: int = config.width
        self.height: int = config.height
        self.grid: list[int] = [15 for _ in range(self.width * self.height)]
        self.pattern_42_coords: set[tuple[int, int]] = (
            self.config.get_absolute_42_coords()
        )

    def get_index(self, x: int, y: int) -> int:
        """Converts coordinates to 1D index"""
        return x + (y * self.width)

    def break_wall(
        self, x1: int, y1: int, x2: int, y2: int, direction: int
    ) -> None:
        index_cell1: int = self.get_index(x1, y1)
        self.grid[index_cell1] &= ~direction
        index_cell2: int = self.get_index(x2, y2)
        self.grid[index_cell2] &= ~self.OPPOSITE[direction]

    def has_wall(self, x: int, y: int, direction: int) -> bool:
        if not (0 <= x < self.width and 0 <= y < self.height):
            return True
        cell_value: int = self.grid[self.get_index(x, y)]
        return bool(cell_value & direction)

    def is_cell_in_42(self, x: int, y: int) -> bool:
        return (x, y) in self.pattern_42_coords
