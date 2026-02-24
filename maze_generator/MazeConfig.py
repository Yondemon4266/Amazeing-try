from typing import Optional
from pydantic import BaseModel, Field, field_validator, model_validator


class MazeConfig(BaseModel):
    width: int = Field(ge=2)
    height: int = Field(ge=2)

    entry: tuple[int, int] = Field(...)
    exit: tuple[int, int] = Field(...)

    perfect: bool = Field(...)

    output_file: str = Field(pattern=r"^[a-zA-Z_]+\.txt$")

    seed: Optional[str] = Field(default=None)
    algorithm: str = "PRIM"

    pattern_width: int = 7 + 2
    pattern_height: int = 5 + 2

    pattern_offsets: list[tuple[int, int]] = [
        # Chiffre 4
        (-3, -2),
        (-3, -1),
        (-3, 0),
        (-2, 0),
        (-1, 0),
        (-1, -2),
        (-1, -1),
        (-1, 1),
        (-1, 2),
        # Chiffre 2
        (1, -2),
        (2, -2),
        (3, -2),
        (3, -1),
        (3, 0),
        (2, 0),
        (1, 0),
        (1, 1),
        (1, 2),
        (2, 2),
        (3, 2),
    ]

    @field_validator("entry", "exit", mode="before")
    @classmethod
    def parse_coords(cls, coords: str) -> tuple[int, int]:
        coords_splitted: list[str] = coords.split(",", 1)
        if len(coords_splitted) != 2:
            raise ValueError(
                "'ENTRY' and 'EXIT' must be 'x,y'"
                f" ints format (received: '{coords_splitted}')"
            )
        x, y = map(int, coords_splitted)
        return (x, y)

    @model_validator(mode="after")
    def validate_logic(self) -> "MazeConfig":
        for name, coord in [("ENTRY", self.entry), ("EXIT", self.exit)]:
            x, y = coord
            if not (0 <= x < self.width) or not (0 <= y < self.height):
                raise ValueError(
                    f"{name} {coord} is out of maze bounds"
                    f" (0-{self.width-1}, 0-{self.height-1})"
                )
        if self.entry == self.exit:
            raise ValueError("ENTRY and EXIT positions must be different.")
        if self.can_fit_42:
            pattern_coords = self.get_absolute_42_coords()
            if self.entry in pattern_coords:
                raise ValueError(
                    f"ENTRY {self.entry} is inside the '42' pattern area."
                )
            if self.exit in pattern_coords:
                raise ValueError(
                    f"EXIT {self.exit} is inside the '42' pattern area."
                )
        else:
            print(
                f"Error: Maze size {self.width}x{self.height} is too "
                "small for '42' pattern."
            )
        return self

    def get_absolute_42_coords(self) -> set[tuple[int, int]]:
        if not self.can_fit_42:
            return set()

        shift_x = (self.width - 7) // 2 - (-3)
        shift_y = (self.height - 5) // 2 - (-2)

        return {(x + shift_x, y + shift_y) for x, y in self.pattern_offsets}

    @property
    def can_fit_42(self) -> bool:
        return (
            self.width >= self.pattern_width
            and self.height >= self.pattern_height
        )
