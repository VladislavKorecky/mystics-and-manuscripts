from colorama import just_fix_windows_console

from mystics_and_manuscripts.game import Game
from mystics_and_manuscripts.level import load_all_levels
from mystics_and_manuscripts.ui.output.display_manager import DisplayManager
from mystics_and_manuscripts.ui.output.scene import Scene
from mystics_and_manuscripts.ui.output.sections.level_achievements import create_achievements_scene
from mystics_and_manuscripts.ui.output.sections.level_menu import LevelMenu
from mystics_and_manuscripts.ui.input import choose_option, Option


# fix colored text on Windows
just_fix_windows_console()

display_manager = DisplayManager()

while True:
    # load all levels found in the "levels" folder
    # this has to be done each time as the level data can be modified at play-through
    levels = load_all_levels()

    menu_scene = Scene()

    # print the menu
    menu = LevelMenu(levels)
    menu_scene.add_sections(menu)
    display_manager.new_scene(menu_scene)

    # let the user pick a level
    options = [Option(i, level.name, level) for i, level in enumerate(levels)] + \
              [Option("a", "Open achievements", "a"), Option("e", "Exit game", "e")]
    option = choose_option(options)

    # show achievements scene
    if option.value == "a":
        display_manager.new_scene(create_achievements_scene(levels))
        display_manager.stop()
        continue

    if option.value == "e":
        exit(0)

    # create and start a new play-through
    game_instance = Game(option.value)
    game_instance.start()
