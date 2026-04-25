from typing import List, Dict, Union
from configparser import ConfigParser
from os import remove


class Parsing:
    """Parses the maze configuration file."""
    def __init__(self, config_file: str) -> None:
        """Initialize the parser with the given config file path."""
        self.WIDTH: int = 0
        self.HEIGHT: int = 0
        self.ENTRY: Dict[str, int] = {}
        self.EXIT: Dict[str, int] = {}
        self.OUTPUT_FILE: str = ""
        self.PERFECT: Union[None, bool] = None
        self.SEED: Union[None, int] = None
        self.CONFIG_FILE: str = config_file

    def set_config(self) -> None:
        """Read and validate the config file, populating all fields."""
        try:
            config: ConfigParser = ConfigParser()
            valid_keys: List[str] = [
                "width",
                "height",
                "entry",
                "exit",
                "output_file",
                "perfect",
                "seed"
            ]

            try:
                with open(self.CONFIG_FILE, 'r') as file:
                    for line in file:
                        if line.startswith('#') or line == "\n":
                            continue
                        parts: List = line.split("=")
                        if parts[0].strip().lower() not in valid_keys:
                            raise ValueError(parts[0].strip())
                        if len(parts) != 2:
                            raise IndexError(line.strip())
            except ValueError as e:
                print(f"Invalid key: {e}")
                exit(0)
            except IndexError as e:
                print(f"Invalid line: {e}")
                exit(0)

            try:
                with open(self.CONFIG_FILE, 'r') as f:
                    config_string: str = '[root]\n' + f.read()
                    config.read_string(config_string)
            except Exception as e:
                print(f"Error loading config data: {e}")
                exit(0)

            try:
                self.SEED = int(config['root']["seed"])
            except KeyError:
                self.SEED = None
            except ValueError as e:
                print(f"Invalid value: {e}")
                exit(0)

            try:
                self.WIDTH = int(config['root']["width"])
                if self.WIDTH < 9 or self.WIDTH > 45:
                    raise ValueError("Invalid width size")
            except KeyError:
                print("Missing value for width")
                exit(0)
            except ValueError as e:
                print(f"Invalid value: {e}")
                exit(0)

            try:
                self.HEIGHT = int(config['root']["height"])
                if self.HEIGHT < 7 or self.HEIGHT > 45:
                    raise ValueError("Invalid height size")
            except KeyError as e:
                print(f"Missing key: {e}")
                exit(0)
            except ValueError as e:
                print(f"Invalid value: {e}")
                exit(0)

            try:
                entry_coords: List = config['root']["entry"].strip().split(",")
                if len(entry_coords) != 2:
                    raise ValueError()
                if entry_coords[0] == "" or entry_coords[1] == "":
                    raise IndexError()
                if (
                    self.WIDTH <= int(entry_coords[0]) or
                    int(entry_coords[0]) < 0 or
                    self.HEIGHT <= int(entry_coords[1]) or
                    int(entry_coords[1]) < 0
                ):
                    raise ValueError("Entry coordinates out of range")
                self.ENTRY = {
                    "x": int(entry_coords[0]),
                    "y": int(entry_coords[1])
                }
            except IndexError:
                print("Missing coordinates in entry")
                exit(0)
            except ValueError as e:
                print(f"Invalid coordinates: {e}")
                exit(0)
            except KeyError as e:
                print(f"Missing: {e}")
                exit(0)

            try:
                exit_coords: List = config['root']["exit"].strip().split(",")
                if len(exit_coords) != 2:
                    raise ValueError()
                if exit_coords[0] == "" or exit_coords[1] == "":
                    raise IndexError()
                if (
                    self.WIDTH <= int(exit_coords[0]) or
                    int(exit_coords[0]) < 0 or
                    self.HEIGHT <= int(exit_coords[1]) or
                    int(exit_coords[1]) < 0
                ):
                    raise ValueError("Exit coordinates out of range")
                self.EXIT = {
                    "x": int(exit_coords[0]),
                    "y": int(exit_coords[1])
                }
            except IndexError:
                print("Missing coordinates in exit")
                exit(0)
            except ValueError as e:
                print(f"Invalid coordinates: {e}")
                exit(0)
            except KeyError as e:
                print(f"Missing: {e}")
                exit(0)

            try:
                if self.ENTRY == self.EXIT:
                    raise ValueError("Entry & exit must not be the same point")
            except ValueError as e:
                print(e)
                exit(0)

            try:
                self.OUTPUT_FILE = str(config['root']["output_file"])
                with open(self.OUTPUT_FILE, "w") as _:
                    remove(self.OUTPUT_FILE)
            except PermissionError:
                print("You have no permission to write in this file")
                exit(0)
            except KeyError as e:
                print(f"Missing: {e}")
                exit(0)

            try:
                is_perfect = config['root']["perfect"]
                if is_perfect in ("True", "TRUE"):
                    self.PERFECT = True
                elif is_perfect in ("False", "FALSE"):
                    self.PERFECT = False
                else:
                    raise ValueError(
                        f"{config['root']['perfect']} is not True or False"
                    )
            except ValueError as e:
                print(f"Invalid value: {e}")
                exit(0)
            except KeyError as e:
                print(f"Missing: {e}")
                exit(0)

        except FileNotFoundError:
            print(f"Config file not found: {self.CONFIG_FILE}")
            exit(0)
        except PermissionError:
            print("You have no permission to read this file")
            exit(0)
        except IndexError as e:
            print(f"Invalid line: {e}")
            exit(0)
        except ValueError as e:
            print(f"Invalid key: {e}")
            exit(0)
        except Exception as e:
            print(f"Error parsing config: {e}")
            exit(0)
