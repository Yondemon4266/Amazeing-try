from MazeConfig import MazeConfig


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

    @classmethod
    def load(cls, filename: str) -> MazeConfig:
        raw_data = cls.read_config_file(filename)

        cls.required_keys_ok(raw_data)

        width = cls.get_int_value("WIDTH", raw_data["WIDTH"])
        height = cls.get_int_value("HEIGHT", raw_data["HEIGHT"])
        entry = cls.get_coord_values("ENTRY", raw_data["ENTRY"])
        exit = cls.get_coord_values("EXIT", raw_data["EXIT"])
        perfect = cls.get_bool_value("PERFECT", raw_data["PERFECT"])
        output_file = cls.get_output_filename(
            "OUTPUT_FILE", raw_data["OUTPUT_FILE"]
        )

        cls.check_min_width_height(width, height)
        cls.check_out_of_limit(entry[0], entry[1], width, height)
        cls.check_out_of_limit(exit[0], exit[1], width, height)

        if entry == exit:
            raise MazeConfigValueError("ENTRY and EXIT must be different.")

        return MazeConfig(
            width=width,
            height=height,
            entry=entry,
            exit=exit,
            perfect=perfect,
            output_file=output_file,
            seed=raw_data.get("SEED"),
            algorithm=raw_data.get("ALGORITHM"),
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
                f"Coordinates x:{x} y:{y} are out of bounds of the maze."
                f"they must be between (0,0) and ({x_max-1},{y_max-1})"
            )
        if x >= x_max or y >= y_max:
            raise MazeConfigError(
                f"Coordinates x:{x} y:{y} are out of bounds of the maze."
                f"they must be between (0,0) and ({x_max-1},{y_max-1})"
            )


def parser():
    try:
        maze_config = MazeConfigParser.load("config.txt")
        print("CONFIG PARSED: ", maze_config.__dict__)

    except MazeConfigError as err:
        print(err.__class__.__name__, err)


if __name__ == "__main__":
    parser()
