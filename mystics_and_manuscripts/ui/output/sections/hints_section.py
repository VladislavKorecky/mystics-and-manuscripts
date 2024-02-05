from mystics_and_manuscripts.ui.output.sections import Section


class HintsSection(Section):
    def __init__(self, hints: list[str]):
        """
        Section of item hints.

        Args:
            hints (list[str]): Hints for paths invalidated by items.
        """

        text = "\n".join(hints)
        super().__init__(text, padding_top=1, padding_bottom=1)
