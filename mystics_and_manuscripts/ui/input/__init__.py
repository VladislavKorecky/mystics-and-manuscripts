class Option:
    def __init__(self, index: int | str, name: str, value):
        """
        An option in a menu.

        Args:
            index (int | str): An index/label unique to this option.
            name (str): Name displayed in the menu.
            value: Value used in code when this option is chosen.
        """

        self.index = str(index)
        self.name = name
        self.value = value


def choose_option(options: list[Option]) -> Option:
    """
    Let the user choose from several options.

    Args:
        options (dict[Option]): Options the user can choose from.

    Returns:
        Option: Chosen option.
    """

    while True:
        user_input = input("I choose ")

        try:
            # find first option that satisfies the user input
            return [option for option in options if option.index == user_input][0]
        except IndexError:
            # when no options are satisfied, using [0] will throw an IndexError
            print(f"Your answer isn't one of the options.")
