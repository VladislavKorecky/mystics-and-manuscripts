from random import choice

from mystics_and_manuscripts.level.achievement import Achievement
from mystics_and_manuscripts.utils import value_or_default


class Place:
    def __init__(self, place: dict):
        """
        A class mirror of the place dictionary.

        Args:
            place (dict): Place data used in this object.
        """

        self.id = place["id"]

        self.name = place["name"]
        self.__description = place["description"]  # accessed by a getter and thus private
        self.first_time_description = place.get("first-time-description")

        self.start = value_or_default(place, "start", False)
        self.end = place.get("end")

        self.items = value_or_default(place, "items", [])

        self.achievement_id = place.get("achievement-id")

        self.call_before = place.get("call-before")
        self.call_after = place.get("call-after")

        self.visited = False

    @property
    def description(self):
        """str: Chosen description depending on context."""

        # check for a first-time description
        if not self.visited and self.first_time_description is not None:
            return self.first_time_description

        # account for multiple descriptions
        if isinstance(self.__description, list):
            return choice(self.__description)

        # default variation
        return self.__description

    @description.setter
    def description(self, value: str | list | None):
        self.__description = value

    # this is a neat trick to allow for dict type casting
    # (https://stackoverflow.com/a/35282286/16343968)
    def __iter__(self):
        yield "id", self.id
        yield "name", self.name
        yield "description", self.__description
        yield "first-time-description", self.first_time_description
        yield "start", self.start
        yield "end", self.end
        yield "items", self.items
        yield "achievement-id", self.achievement_id
        yield "call-before", self.call_before
        yield "call-after", self.call_after
