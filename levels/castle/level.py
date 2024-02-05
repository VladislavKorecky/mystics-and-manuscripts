from mystics_and_manuscripts.game import Game
from mystics_and_manuscripts.level import Action, Path, Achievement

fake_throne_room_discovered = False
drink_wine_attempts = 0


def create_ladder(game: Game):
    """
    Create the ladder item once the hole in the ground of the first floor is discovered.

    Args:
        game (Game): Reference to the game state.
    """

    # get the first-floor hall room reference
    hall = game.level.get_place_by_id(56)

    # get the armory room reference
    armory = game.level.get_place_by_id(42)

    # check if the place was already discovered or not
    if armory.visited:
        armory.description = "I got it! I could use the siege ladder as a way across."
    else:
        armory.description = "Here is where all the army's equipment is stored. Most of it got looted, but some " \
                            "weapons are still lying around. In the corner is a siege ladder. I got it! That could " \
                            "come in handy for that hole on the first floor."

    # add the item
    armory.items.append("ladder")

    # prepare the cleanup
    hall.call_after = None
    armory.call_after = "ladder_pickup_cleanup"


def ladder_pickup_cleanup(game: Game):
    """
    Replace the armory's description after the player acquires the ladder. This is done so that the player doesn't see
    the discovery message twice.

    Args:
        game (Game): Reference to the game state.
    """

    # get the armory room reference
    place = game.level.get_place_by_id(42)

    place.description = "Since I already took the ladder, the room doesn't have much more to offer."


def discover_fake_throne_room(game: Game):
    """
    Note that the fake throne room was discovered for future use.

    Args:
        game (Game): Reference to the game state.
    """

    global fake_throne_room_discovered
    fake_throne_room_discovered = True


def unsuccessful_search(game: Game):
    """
    An action called "Look for secret passage" available in all rooms except the Ancestral Chamber.

    Args:
        game (Game): Reference to the game state.
    """

    return "You think the secret passage could be right here, but no matter how hard you look, there seems to be " \
           "nothing to find."


def sit_and_ponder(game: Game):
    """
    An action on the watch tower.

    Args:
        game (Game): Reference to the game state.
    """

    # check if the action already exists, otherwise, duplicates would appear
    look_for_passage_action = next((a for a in game.level.actions if a.function == "unsuccessful_search"), None)

    if fake_throne_room_discovered and look_for_passage_action is None:
        # add the unsuccessful "Look for secret passage" action
        game.level.actions.append(
            Action({
                "name": "Look for secret passage",
                # get every place except the Ancestral Chamber
                # the dict conversion is needed because the Action doesn't take objects
                "places": [place.id for place in game.level.places if place.id != 54],
                "function": "unsuccessful_search"
            })
        )

        # add the successful path
        game.level.paths.append(Path({
            "name": "Look for secret passage",
            "places": [54, 55],
            "description": "Heureka! Where else to put the secret room than right to your ancestors? You start taking "
                           "the portraits one by one. Although you think the idea is genius, you still feel surprised "
                           "when there's a hole to the throne room."
        }))

        return "The calming view from the tower and the soft, cold wind are the perfect combination for deep " \
               "thinking. Your mind escapes into a sea of imagination when it is suddenly interrupted. Your eyes are " \
               "locked on what appears to be a window of the throne room. The window shows the purple throne; wait " \
               "... weren't the cushions green?! Not to mention it being on the wrong side of the castle. At first, " \
               "you think your mind is tricking you, but it's not; you remember it correctly: the throne was green " \
               "and on the opposite side. There's only one explanation - a secret room."

    return "The calming view from the tower and the soft, cold wind are the perfect combination for deep thinking. " \
           "You look up into the sky and ponder life's most daunting questions."


def drink_wine(game: Game):
    # increment attempt
    global drink_wine_attempts
    drink_wine_attempts += 1

    # get the associated text
    if drink_wine_attempts == 1:
        attempt = "first"
    elif drink_wine_attempts == 2:
        attempt = "second"
    else:
        attempt = "third"

    if drink_wine_attempts == 3:
        # award an achievement
        wine_cellar = game.level.get_place_by_id(41)
        wine_cellar.achievement_id = 7

        # remove the action
        action_index = next(i for i, action in enumerate(game.level.actions) if action.name == "Drink wine")
        game.level.actions.pop(action_index)

    return f"You break the {attempt} barrel to taste a mouthful of wine, but it's empty."
