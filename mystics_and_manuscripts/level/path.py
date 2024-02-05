from random import choice

from mystics_and_manuscripts.level.achievement import Achievement
from mystics_and_manuscripts.utils import value_or_default


class Path:
    def __init__(self, path: dict):
        """
        A class mirror of the path dictionary.

        Args:
            path (dict): Path data used in this object.
        """

        self.places = path["places"]

        self.name = value_or_default(path, "name", "Unnamed path")
        self.__description = path.get("description")
        self.first_time_description = path.get("first-time-description")

        self.one_way = value_or_default(path, "one-way", False)
        self.one_way_start = path.get("one-way-start")

        self.disable_go_back = value_or_default(path, "disable-go-back", False)

        self.required_items = value_or_default(path, "required-items", [])
        self.forbidden_items = value_or_default(path, "forbidden-items", [])
        self.items_hint = value_or_default(path, "items-hint", False)

        self.achievement_id = path.get("achievement-id")

        self.visited = False

    @property
    def description(self):
        """str: Chosen description depending on context."""

        # check for default value use
        if self.__description is None:
            return "You walk along a path."

        # check for a first-time description
        if not self.visited and self.first_time_description is not None:
            return self.first_time_description

        # account for multiple descriptions
        if isinstance(self.__description, list):
            return choice(self.__description)

        return self.__description

    @description.setter
    def description(self, value: str | list | None):
        self.__description = value

    # this is a neat trick to allow for dict type casting
    # (https://stackoverflow.com/a/35282286/16343968)
    def __iter__(self):
        yield "places", self.places
        yield "name", self.name
        yield "description", self.__description
        yield "first-time-description", self.first_time_description
        yield "one-way", self.one_way
        yield "one-way-start", self.one_way_start
        yield "disable-go-back", self.disable_go_back
        yield "required-items", self.required_items
        yield "forbidden-items", self.forbidden_items
        yield "items-hint", self.items_hint
        yield "achievement-id", self.achievement_id
