from mystics_and_manuscripts.level import Path, Action
from mystics_and_manuscripts.ui.output.sections import Section


class OptionsMenu(Section):
    def __init__(self, paths: list[Path], actions: list[Action], last_path: Path):
        """
        Print a selection menu for paths and actions.

        Args:
            paths (list[Path]): List of paths.
            actions (list[Action]): List of actions.
            last_path (Path): Last used path.
        """

        menu_items = []

        # adding paths
        for i, path in enumerate(paths):
            path_name = path.name

            # figure out if the "(Go back)" hint should be included
            go_back_hint = '(Go back)' if last_path is path and not path.disable_go_back else ''

            menu_items.append(f"{i}. {path_name} {go_back_hint}")

        # adding actions
        for i, action in enumerate(actions):
            action_name = action.name
            menu_items.append(f"{len(paths) + i}. {action_name}")

        super().__init__("\n".join(menu_items), padding_top=1, padding_bottom=1)
