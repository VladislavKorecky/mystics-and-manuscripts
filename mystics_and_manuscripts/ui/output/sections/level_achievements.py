import json

from colorama import Style

from mystics_and_manuscripts.level import Level
from mystics_and_manuscripts.ui.output.scene import Scene
from mystics_and_manuscripts.ui.output.sections import Section


def create_achievements_scene(levels: list[Level]) -> Scene:
    """
    Create a scene with all unlocked achievements.

    Args:
        levels (list[Level]): Levels to get achievements from.

    Returns:
        Scene: Scene with unlocked achievements.
    """

    scene = Scene()

    for level in levels:
        scene.add_sections(LevelAchievements(level))

    return scene


class LevelAchievements(Section):
    def __init__(self, level: Level):
        """
        Section with all unlocked achievements from a level.

        Args:
            level (Level): Level to get achievements from.
        """

        # get all level achievements and the file with unlocked achievements
        achievements = level.achievements
        achievements_file = level.achievements_file_path

        # base assumption: achievements file doesn't exist
        unlocked_achievements_ids = []

        # load unlocked achievements
        if achievements_file.is_file():
            with open(achievements_file, "r") as f:
                unlocked_achievements_ids = json.load(f)

        # turn achievement IDs into achievement objects
        unlocked_achievements = [a for a in achievements if a.id in unlocked_achievements_ids]

        # add name of the level and general info
        text = f"{Style.BRIGHT}{level.name}{Style.RESET_ALL} ({len(unlocked_achievements)}/{len(achievements)})"

        # add a line for every unlocked achievement
        for achievement in unlocked_achievements:
            text += f"\n{achievement.name} - {achievement.description}"

        super().__init__(text, padding_top=1, padding_bottom=1)
