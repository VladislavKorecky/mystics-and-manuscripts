class Scene:
    def __init__(self):
        """
        Scene made up of sections.
        """

        self.sections = []

    def add_sections(self, *args):
        """
        Add new sections to the scene.

        Args:
            *args: Sections to add.
        """

        self.sections.extend(args)

    def to_text(self) -> str:
        """
        Combine the scene's sections into one block of text. The higher number is used when two section paddings
        overlap.

        Returns:
            str: Section contents and paddings in one text.
        """

        if len(self.sections) == 0:
            return ""

        first_section = self.sections[0]

        text = first_section.to_text()
        bottom_padding = first_section.padding_bottom

        for section in self.sections[1:]:
            if section.padding_top < bottom_padding:
                text += section.to_text(disable_top_padding=True)
                bottom_padding = section.padding_bottom
                continue

            # remove previous bottom padding
            # note: the if condition is there because -0 index doesn't work and just deletes the whole text
            text = text if bottom_padding == 0 else text[:-bottom_padding]

            text += section.to_text()
            bottom_padding = section.padding_bottom

        return text
