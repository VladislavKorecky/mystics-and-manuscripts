from mystics_and_manuscripts.level import Level
from mystics_and_manuscripts.ui.output.sections import Section


class LevelMenu(Section):
    def __init__(self, levels: list[Level]):
        """
            Print a selection menu for the levels.

            Args:
                levels (list[Level]): List of levels.
            """

        text = "\n".join([f"{i}. {level.name}" for i, level in enumerate(levels)])

        # add extra options
        text += "\ne. Exit game"
        text += "\na. Open achievements"

        super().__init__(text)
