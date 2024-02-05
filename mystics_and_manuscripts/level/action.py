class Action:
    def __init__(self, action: dict):
        """
        A class mirror of the action dictionary.

        Args:
            action (dict): Action data used in this object.
        """

        self.name = action["name"]
        self.places = action["places"]
        self.function = action["function"]

    # this is a neat trick to allow for dict type casting
    # (https://stackoverflow.com/a/35282286/16343968)
    def __iter__(self):
        yield "name", self.name
        yield "places", self.places
        yield "function", self.function
