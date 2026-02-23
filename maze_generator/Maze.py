class Maze:
    NORTH = 1  # 0001
    EAST = 2  # 0010
    SOUTH = 4  # 0100
    WEST = 8  # 1000

    OPPOSITE = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}

    def __init__(self, width: int, height: int) -> None:
        self.width: int = width
        self.height: int = height
        self.grid: list[int] = [15 for _ in range(width * height)]

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
