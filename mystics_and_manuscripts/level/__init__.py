from glob import glob
from random import choice

from yaml import safe_load

from mystics_and_manuscripts.level.achievement import Achievement
from mystics_and_manuscripts.level.action import Action
from mystics_and_manuscripts.level.place import Place
from mystics_and_manuscripts.level.path import Path

from pathlib import Path as FilePath

from mystics_and_manuscripts.utils import mirror_or_empty


class Level:
    def __init__(self, level: dict, path_to_level: str):
        """
        A class mirror of the level dictionary.

        Args:
            level (dict): Level data used in this object.
            path_to_level (str): Path to the level's folder.
        """

        self.name = level["name"]
        self.introduction = level.get("introduction")
        self.places = [Place(place_dict) for place_dict in level["places"]]
        self.paths = mirror_or_empty(level, "paths", Path)
        self.actions = mirror_or_empty(level, "actions", Action)
        self.achievements = mirror_or_empty(level, "achievements", Achievement)

        self.level_file_path = FilePath(path_to_level)
        self.folder_path = self.level_file_path.parent

        # note: adding a file/sub-folder to a pathlib "Path" is done using a slash
        self.achievements_file_path = self.folder_path / "achievements.json"

    def get_place_by_id(self, place_id: int) -> Place | None:
        """
        Find a place by its ID.

        Args:
            place_id (int): ID of the place to look for.

        Returns:
            dict | None: The place with the ID or None if the place doesn't exist in the level.
        """

        for place_obj in self.places:
            if place_obj.id == place_id:
                return place_obj

        return None

    def find_starting_places(self) -> list[Place]:
        """
        Return a list of starting places of a level.

        Returns:
            list[Place]: List of starting places.
        """

        return [place_obj for place_obj in self.places if place_obj.start]

    def pick_starting_place(self) -> Place:
        """
        Randomly choose a starting place of a level.

        Returns:
            Place: Randomly chosen starting place.
        """

        return choice(self.find_starting_places())


def get_all_level_paths() -> list[str]:
    """
    Get all level paths from the "levels" folder.

    Returns:
        list[str]: List of paths to level yaml files.
    """

    return glob("levels/*/level.yaml") + glob("levels/*/level.yml")


def load_levels(level_paths: list[str]) -> list[Level]:
    """
    Load levels from their paths.

    Args:
        level_paths (list[str]): List of paths to the level files.

    Returns:
        list[Level]: List of level objects.
    """

    levels = []

    for lvl_path in level_paths:
        with open(lvl_path, "r") as f:
            level_dict = safe_load(f)
            levels.append(Level(level_dict, lvl_path))

    return levels


def load_all_levels() -> list[Level]:
    """
    Load all levels from the "levels" folder.

    Returns:
        list[Level]: List of level objects.
    """

    return load_levels(get_all_level_paths())
