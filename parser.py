from typing import Optional


class MazeConfigError(Exception):
    pass


class MazeConfigKeyError(MazeConfigError):
    pass


class MazeConfigValueError(MazeConfigError):
    pass


class MazeConfigFileError(MazeConfigError, OSError):
    pass


class MazeConfigParser:
    required_keys: list[str] = [
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
    ]
    optional_keys: list[str] = ["SEED", "ALGORITHM", "DISPLAY_MODE"]

    def __init__(self, filename: str) -> None:
        self.width: int
        self.height: int
        self.entry: tuple[int, int]
        self.exit: tuple[int, int]
        self.perfect: bool
        self.output_file: str
        self.seed: Optional[str]
        self.algorithm: Optional[str]
        self.display_mode: Optional[str]
        self.option_added: bool = False
        self.read_parse_maze_config(filename)

    def read_parse_maze_config(self, filename: str) -> None:

        config: dict[str, str] = self.read_config_file(filename)
        print(config)
        self.required_keys_ok(config)
        int_keys = ["WIDTH", "HEIGHT"]
        coord_keys = ["ENTRY", "EXIT"]

        for key in int_keys:
            setattr(self, key.lower(), self.get_int_value(key, config[key]))

        for key in coord_keys:
            setattr(self, key.lower(), self.get_coord_values(key, config[key]))

        self.perfect = self.get_bool_value("PERFECT", config["PERFECT"])
        self.output_file = self.get_output_filename(
            "OUTPUT_FILE", config["OUTPUT_FILE"]
        )

        self.check_min_width_height(self.width, self.height)
        self.check_out_of_limit(
            self.entry[0], self.entry[1], self.width, self.height
        )
        self.check_out_of_limit(
            self.exit[0], self.exit[1], self.width, self.height
        )

    @staticmethod
    def read_config_file(filename: str) -> dict[str, str]:
        try:
            config: dict[str, str] = {}
            with open(filename, "r") as file:
                for line in file:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" not in line:
                        continue
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()
                    config[key] = value
        except OSError as err:
            raise MazeConfigFileError(f"'{filename}' -> {err.strerror}")
        return config

    @staticmethod
    def required_keys_ok(config: dict[str, str]) -> bool:
        missing_keys = [
            key for key in MazeConfigParser.required_keys if key not in config
        ]
        if missing_keys:
            raise MazeConfigKeyError(
                "Some required keys are missing in config file "
                f"[keys: {', '.join(missing_keys)}]"
            )
        return True

    @staticmethod
    def get_int_value(key: str, value: str) -> int:
        try:
            return int(value)
        except ValueError:
            raise MazeConfigValueError(
                f"Value of '{key}' must be an integer (received: '{value}')"
            )

    @staticmethod
    def get_coord_values(key: str, value: str) -> tuple[int, int]:
        try:
            x, y = map(int, value.split(","))
            return (x, y)
        except ValueError:
            raise MazeConfigValueError(
                f"'{key}' must be 'x,y' ints format (received: '{value}')"
            )

    @staticmethod
    def get_bool_value(key: str, value: str) -> bool:
        if value.lower() not in ["true", "false"]:
            raise MazeConfigValueError(
                f"'{key}' must be 'true' or 'false' (received: '{value}')"
            )
        return value.lower() == "true"

    @staticmethod
    def get_output_filename(key: str, value: str) -> str:
        from re import match as regex_match

        if not regex_match(r"^[a-zA-Z_]+\.txt$", value):
            raise MazeConfigValueError(
                f"Invalid output filename for '{key}': '{value}'. "
                "Must contain only letters and underscores, "
                "and end with '.txt' (no digits allowed)."
            )
        return value

    @staticmethod
    def check_min_width_height(width: int, height: int) -> None:
        if width < 2 or height < 2:
            raise MazeConfigValueError(
                "Width and height of the maze must be >= 2"
            )

    @staticmethod
    def check_out_of_limit(x: int, y: int, x_max: int, y_max: int) -> None:
        if x < 0 or y < 0:
            raise MazeConfigError(
                f"Coordinates x:{x} y:{y} must be in the bounds of "
                f"the maze ({x_max},{y_max})"
            )
        if x > x_max or y > y_max:
            raise MazeConfigError(
                f"Coordinates x:{x} y:{y} must be in the bounds of"
                f"the maze ({x_max},{y_max})"
            )


def parser():
    try:
        maze_config = MazeConfigParser("config.txt")
        print(maze_config.__dict__)

    except MazeConfigError as err:
        print(err.__class__.__name__, err)


if __name__ == "__main__":
    parser()
