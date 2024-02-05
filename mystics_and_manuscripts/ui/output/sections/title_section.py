from mystics_and_manuscripts.ui.output.sections import Section


class TitleSection(Section):
    def __init__(self, content: str):
        """
        Section for quick title creation.

        Args:
            content (str): Text to put in the title.
        """

        title_length = len(content)
        separator_length = title_length + 8

        text = "-" * separator_length + "\n" + " " * 4 + content + "\n" + "-" * separator_length
        super().__init__(text)
