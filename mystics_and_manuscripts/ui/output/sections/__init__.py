class Section:
    def __init__(self, content: str, padding_top: int = 0, padding_bottom: int = 0):
        """
        Section/Paragraph of a text.

        Args:
            content (str): Text content of the section.
            padding_top (int, optional): Number of empty lines above the content. Default: 0
            padding_bottom (int, optional): Number of empty lines below the content. Default: 0
        """

        self.__content = content
        self.padding_top = padding_top
        self.padding_bottom = padding_bottom

    def to_text(self, disable_top_padding: bool = False) -> str:
        """
        Return a text representation of the section.

        Args:
            disable_top_padding (bool, optional): True to disable top padding. Default: False

        Returns:
            str: Content with top and bottom paddings.
        """

        # remove trailing new-lines from the end
        content = self.__content.rstrip("\n")

        # the +1 after padding_bottom is just so that the next section's text is on another line
        # only after that can you add emtpy lines
        # otherwise, if you concat the text it's all going to be on one line and not as separate sections
        return "\n" * (0 if disable_top_padding else self.padding_top) \
            + content \
            + "\n" * (self.padding_bottom + 1)
