class Maze:
    NORTH = 1  # 0001
    EAST = 2  # 0010
    SOUTH = 4  # 0100
    WEST = 8  # 1000

    def __init__(self, width: int, height: int) -> None:
        self.width: int = width
        self.height: int = height
        self.grid: list[int] = [15 for _ in range(width * height)]

        def get_index(self, x: int, y: int) -> int:
            """Converts coordinates to 1D index"""
            return x + (y * self.width)

        def break_wall(self, x: int, y: int, direction: int) -> None:
            self.grid[idx] &= ~direction
