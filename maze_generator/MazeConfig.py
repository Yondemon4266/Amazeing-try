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
        return self
