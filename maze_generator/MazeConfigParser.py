from maze_generator.MazeConfig import MazeConfig
from pydantic import ValidationError
from typing import cast


class MazeConfigFileError(OSError):
    pass


class MazeConfigParser:
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
                    config[key.lower()] = value
        except OSError as err:
            raise MazeConfigFileError((f"'{err.filename}' -> {err.strerror}"))
        return config

    @classmethod
    def load(cls, filename: str) -> MazeConfig:
        raw_data = cls.read_config_file(filename)
        return cast(MazeConfig, MazeConfig.model_validate(raw_data))


def parser() -> None:
    try:
        maze_config = MazeConfigParser.load("config.txt")
        print("CONFIG PARSED: ", maze_config.__dict__)

    except ValidationError as err:
        for error in err.errors():
            field = " -> ".join(map(str, error["loc"])).upper()
            msg: str = error.get("msg", "empty")
            input_val = error.get("input", "empty")
            print(
                f"MazeConfig error, Field {field} : "
                f"{msg} (received value : '{input_val}')"
            )
    except OSError as err:
        print(err)


if __name__ == "__main__":
    parser()
