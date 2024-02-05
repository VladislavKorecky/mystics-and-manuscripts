class Achievement:
    def __init__(self, achievement: dict):
        """
        A class mirror of the achievement dictionary.

        Args:
            achievement (dict): Achievement data used in this object.
        """

        self.id = achievement["id"]
        self.name = achievement["name"]
        self.description = achievement["description"]

    # this is a neat trick to allow for dict type casting
    # (https://stackoverflow.com/a/35282286/16343968)
    def __iter__(self):
        yield "name", self.name
        yield "description", self.description
