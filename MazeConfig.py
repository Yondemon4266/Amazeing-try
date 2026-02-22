from typing import Optional


class MazeConfig:

    def __init__(
        self,
        width,
        height,
        entry,
        exit,
        perfect,
        output_file,
        seed=None,
        algorithm=None,
        display_mode=None,
    ):
        self.width: int = width
        self.height: int = height
        self.entry: tuple[int, int] = entry
        self.exit: tuple[int, int] = exit
        self.perfect: bool = perfect
        self.output_file: str = output_file
        self.seed: Optional[str] = seed
        self.algorithm: Optional[str] = algorithm
        self.display_mode: Optional[str] = display_mode
