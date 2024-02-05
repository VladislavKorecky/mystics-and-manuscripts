import os

from mystics_and_manuscripts.ui.output.scene import Scene
from mystics_and_manuscripts.utils import Singleton


class DisplayManager(metaclass=Singleton):
    def __init__(self):
        """
        Manager of all visuals.
        """

        self.current_scene = Scene()

    @staticmethod
    def stop() -> None:
        """
        Stop the execution of the code and wait for the player to press ENTER.
        """

        input("Press ENTER to continue...")

    def __update(self):
        """
        Update the text in the console.
        """

        # clear console based on the operating system
        os.system('cls' if os.name == 'nt' else 'clear')

        text = self.current_scene.to_text()
        print(text, end="")

    def new_scene(self, scene: Scene):
        """
        Replace the current scene by a new one.
        """

        self.current_scene = scene
        self.__update()
