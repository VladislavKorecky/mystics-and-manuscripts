import json
from importlib import import_module
from random import choice
from string import ascii_lowercase

from colorama import Back, Style

from mystics_and_manuscripts.level import Level, Place, Path, Achievement
from mystics_and_manuscripts.level.action import Action
from mystics_and_manuscripts.ui.output.display_manager import DisplayManager
from mystics_and_manuscripts.ui.output.scene import Scene
from mystics_and_manuscripts.ui.output.sections import Section
from mystics_and_manuscripts.ui.output.sections.hints_section import HintsSection
from mystics_and_manuscripts.ui.output.sections.options_menu import OptionsMenu
from mystics_and_manuscripts.ui.output.sections.title_section import TitleSection


class Game:
    def __init__(self, level: Level) -> None:
        """
        Object containing play-through information and necessary functions.

        Args:
            level (Level): Level being played.
        """

        self.level = level

        self.inventory = []  # list of items that the player holds
        self.last_path = None  # last path used
        self.current_place = None  # data of the current place where the player resides

        self.display_manager = DisplayManager()

        # only load the level script if it exists
        if (level.folder_path / "level.py").is_file():
            self.level_script = import_module(f"levels.{level.folder_path.name}.level")

    @staticmethod
    def create_place_scene(place: Place) -> Scene:
        """
        Create a place scene.

        Args:
            place (Place): Place to display.

        Returns:
            Scene: Scene with info about a place.
        """

        scene = Scene()

        entry_section = Section(f"You've entered {place.name}", padding_bottom=1)
        title = TitleSection(place.name)
        description = Section(place.description, padding_bottom=1)

        scene.add_sections(entry_section, title, description)
        return scene

    @staticmethod
    def create_path_scene(path: Path) -> Scene:
        """
        Create a scene about a path.

        Args:
            path (Path): Path to extract the information from.

        Returns:
            Scene: Scene with path information.
        """

        scene = Scene()
        scene.add_sections(Section(path.description, padding_bottom=1))
        return scene

    @staticmethod
    def create_action_scene(action_message: str):
        """
        Create a scene about an action.

        Args:
            action_message (str): Message when you execute an action.

        Returns:
            Scene: Scene with action information.
        """

        scene = Scene()
        scene.add_sections(Section(action_message, padding_bottom=1))
        return scene

    @staticmethod
    def select_path_or_action(
            available_paths: list[Path], available_actions: list[Action]) -> tuple[Path | None, Action | None]:
        """
        Make the user choose a path to go through or an action to take.

        Args:
            available_paths (list[Path]): List of available paths from the current location.
            available_actions (list[Action]): List of available actions in the current location.

        Returns:
            tuple: A chosen path at index 0 and a chosen action at index 1. One of them will always be None.
        """

        error_message = f"You must enter a number between 0 and {len(available_paths) + len(available_actions) - 1}"
        
        option_index = None

        # ask user until a correct answer is given
        while True:
            user_input = input("I choose ")

            # check the option is a number
            try:
                option_index = int(user_input)
            except ValueError:
                print(error_message)
                continue

            # check the option is within range
            if option_index < len(available_paths) + len(available_actions):
                break

            print(error_message)

        # check if the index is part of the paths or actions
        if option_index < len(available_paths):
            return available_paths[option_index], None

        action_index = option_index - len(available_paths)
        return None, available_actions[action_index]

    def get_available_paths(self) -> list[Path]:
        """
        Return a list of available paths from the current place.

        Returns:
            list[Path]: List of paths that can be used from the current location.
        """

        def is_valid(path) -> bool:
            # check that the path is connected to the current place
            if self.current_place.id not in path.places:
                return False

            # check that the path is bidirectional or is one way from the current place
            if path.one_way and self.current_place.id not in path.one_way_start:
                return False

            return True

        return [path for path in self.level.paths if is_valid(path)]

    @staticmethod
    def add_hint_message(path: Path, items: list[str], hints: list[str], problem: str):
        """
        Add a new hint message to the hints.

        Args:
            path (Path): The path that requires/forbids certain items.
            items (list[str]): Items that are incompatible.
            hints (list[str]): Existing list of hints.
            problem (str): Problem message. (e.g. "Missing" or "Can't have")
        """

        letter_index = ascii_lowercase[len(hints) % 26]  # turn the hint's index into a letter
        hints.append(f"{letter_index}. {path.name} ({problem}: {', '.join(items)})")

    def check_for_required_items(self, required_items: list[str], hints: list[str], path: Path) -> bool:
        """
        Check if the player has all required items.

        Args:
            required_items (list[str]): List of required items.
            hints (list[str]): List of previous hints.
            path (Path): Path with the required items.

        Returns:
            bool: True if path was invalidated, False otherwise.
        """

        remaining_required_items = [item for item in required_items if item not in self.inventory]

        if len(remaining_required_items) == 0:
            return False

        if path.items_hint:
            Game.add_hint_message(path, remaining_required_items, hints, "Missing")

        return True

    def check_for_forbidden_items(self, forbidden_items: list[str], hints: list[str], path: Path) -> bool:
        """
        Check if the player has a forbidden item.

        Args:
            forbidden_items (list[str]): List of forbidden items.
            hints (list[str]): List of previous hints.
            path (Path): Path with forbidden items.

        Returns:
            bool: True if path is invalid, False otherwise.
        """

        owned_forbidden_items = [item for item in forbidden_items if item in self.inventory]

        if len(owned_forbidden_items) == 0:
            return False

        if path.items_hint:
            Game.add_hint_message(path, owned_forbidden_items, hints, "Can't have")

        return True

    def separate_unusable_item_paths(self, available_paths: list[Path]) -> tuple:
        """
        Create hints for paths with missing/forbidden items and separate them.

        Args:
            available_paths (list[Path]): List of available paths from the current location.

        Returns:
            tuple: List of hints for invalid paths at index 0 and new list of available paths at index 1.
        """

        hints = []

        def is_valid(path: Path) -> bool:
            required_items = path.required_items
            forbidden_items = path.forbidden_items

            # check for required items
            path_invalidated = self.check_for_required_items(required_items, hints, path)

            # check for forbidden items
            if not path_invalidated:
                path_invalidated = self.check_for_forbidden_items(forbidden_items, hints, path)

            return not path_invalidated

        new_available_paths = [p for p in available_paths if is_valid(p)]
        return hints, new_available_paths

    def move_player(self, path: Path):
        """
        Move the player from its current position along a path to a new place.

        Args:
            path (Path): Chosen path to move along.
        """

        # create a copy of the "places" attribute in the path
        destinations = path.places.copy()

        # remove the current place from the list of possible destinations
        destinations.remove(self.current_place.id)

        # choose a random destination
        new_place_id = choice(destinations)

        self.current_place = self.level.get_place_by_id(new_place_id)

    def check_end_conditions(self, scene: Scene) -> bool:
        """
        Check for an ending and add a section to the scene if so.

        Args:
            scene (Scene): A section will be added to the scene if the game ended.

        Returns:
            bool: True if the game ended, False otherwise.
        """

        ending = self.current_place.end

        if ending:
            if ending == "win":
                scene.add_sections(Section(f"{Back.GREEN}YOU WON!{Back.RESET}", padding_top=1))
                return True

            if ending == "loss":
                scene.add_sections(Section(f"{Back.RED}YOU LOST!{Back.RESET}", padding_top=1))
                return True

            if ending == "draw":
                scene.add_sections(Section(f"{Back.WHITE}YOU DREW!{Back.RESET}", padding_top=1))
                return True

        return False

    def add_items(self, scene: Scene):
        """
        Add items from a place to the player's inventory.

        Args:
            scene (Scene): A section with acquired items will be added if any new items were received.
        """

        items = self.current_place.items

        if items is None or len(items) == 0:
            return

        section_text = ""

        for item in items:
            if item in self.inventory:
                continue

            section_text += f"{Style.BRIGHT}ITEM ACQUIRED:{Style.RESET_ALL} {item}"
            self.inventory.append(item)

        # display the acquired items
        section = Section(section_text, padding_top=1, padding_bottom=1)
        scene.add_sections(section)

    def create_introduction_scene(self) -> Scene:
        """
        Create a scene with the level introduction.

        Returns:
            Scene: Scene with the introduction.
        """

        scene = Scene()

        # display the title
        title_section = TitleSection(self.level.name)
        scene.add_sections(title_section)

        # display level description
        intro_text = self.level.introduction
        if intro_text is not None:
            scene.add_sections(Section(intro_text, padding_bottom=1))

        return scene

    def get_available_actions(self) -> list[Action]:
        """
        Return all available actions form the current place.

        Returns:
            list[dict]: Available actions to take.
        """

        actions = self.level.actions
        return [action for action in actions if self.current_place.id in action.places]

    def init_achievements_file(self):
        """
        Create a new file for storing achievements.
        """

        with open(self.level.achievements_file_path, "w") as f:
            json.dump([], f)

    def get_achievement_by_id(self, achievement_id: int) -> Achievement | None:
        """
        Return an achievement with a specific ID.

        Args:
            achievement_id (int): ID of the target achievement.

        Returns:
            Achievement: Achievement object or None if not found.
        """

        for achievement in self.level.achievements:
            if achievement.id == achievement_id:
                return achievement

        return None

    def add_achievement_from_place(self, place: Place, scene: Scene):
        """
        Award the player an achievement from a place.

        Args:
            place (Place): Place with the achievement.
            scene (Scene): Scene for displaying the added achievement.
        """

        with open(self.level.achievements_file_path, "r") as f:
            existing_achievements = json.load(f)

        if place.achievement_id is None:
            return

        if place.achievement_id in existing_achievements:
            return

        # add the achievement to unlocked achievements
        existing_achievements.append(place.achievement_id)

        with open(self.level.achievements_file_path, "w") as f:
            json.dump(existing_achievements, f)

        # get the related achievement object
        achievement = self.get_achievement_by_id(place.achievement_id)

        # add the achievement to the scene
        scene.add_sections(Section(
            f"{Style.BRIGHT}ACHIEVEMENT UNLOCKED:{Style.RESET_ALL} "
            f"{achievement.name} - {achievement.description}",
            padding_top=1,
            padding_bottom=1
        ))

    def run_function_if_exists(self, function_name: str) -> None:
        """
        Run a function from the level script if it exists.

        Args:
            function_name (str): Name of the function to call.
        """

        if function_name is None:
            return

        try:
            getattr(self.level_script, function_name)(self)
        except AttributeError:
            pass

    def start(self) -> None:
        """
        Start a new level play-through.
        """

        # create a new achievements file if it doesn't exist yet
        if not self.level.achievements_file_path.is_file():
            self.init_achievements_file()

        # run the level's on start function
        self.run_function_if_exists("on_start")

        # print the introduction to the level
        introduction = self.create_introduction_scene()
        self.display_manager.new_scene(introduction)
        self.display_manager.stop()

        # randomly choose between the starting places
        self.current_place = self.level.pick_starting_place()

        # game loop
        while True:
            # call custom "before" function
            self.run_function_if_exists(self.current_place.call_before)

            place_scene = self.create_place_scene(self.current_place)

            # mark the current place as visited
            self.current_place.visited = True

            # add any new achievements
            self.add_achievement_from_place(self.current_place, place_scene)

            # check the ending conditions
            end = self.check_end_conditions(place_scene)

            if end:
                self.display_manager.new_scene(place_scene)
                self.display_manager.stop()
                break

            # add any items to the player's inventory
            self.add_items(place_scene)

            # prepare paths and actions
            available_paths = self.get_available_paths()
            hints, available_paths = self.separate_unusable_item_paths(available_paths)
            available_actions = self.get_available_actions()

            # call custom "after" function
            self.run_function_if_exists(self.current_place.call_after)

            # visualize path information
            if len(hints) > 0:
                hints_section = HintsSection(hints)
                place_scene.add_sections(hints_section)

            option_menu = OptionsMenu(available_paths, available_actions, self.last_path)
            place_scene.add_sections(option_menu)

            # update the scene to display all changes
            self.display_manager.new_scene(place_scene)

            # let the user select a path
            path, action = Game.select_path_or_action(available_paths, available_actions)

            # handle an action
            if action is not None:
                action_func = getattr(self.level_script, action.function)
                action_message = action_func(self)

                scene = self.create_action_scene(action_message)
                self.display_manager.new_scene(scene)
                self.display_manager.stop()

                continue

            self.last_path = path

            # display the path info
            path_scene = self.create_path_scene(path)
            self.display_manager.new_scene(path_scene)
            self.display_manager.stop()

            # mark path as visited
            path.visited = True

            # move the player to a new destination
            self.move_player(path)
