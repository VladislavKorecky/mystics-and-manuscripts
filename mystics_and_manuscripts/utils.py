from typing import Type


def value_or_default(dictionary: dict, key, default):
    """
    Return a retrieved value from dictionary or its default when None.

    Args:
        dictionary (dict): Dictionary to retrieve from.
        key: Key in the dictionary.
        default: Value to return if the retrieved item is None.

    Returns:
        Non-none values.
    """

    return dictionary.get(key) if dictionary.get(key) is not None else default


def mirror_or_empty(dictionary: dict, key, mirror_class: Type) -> list:
    """
    Convert list items to their mirror if the list isn't None, return an empty list otherwise.

    Args:
        dictionary (dict): Dictionary where the list resides.
        key: Key of the list.
        mirror_class (Type): Class mirror to convert to.

    Returns:
        list: List of mirrored items or empty list.
    """

    return [mirror_class(item) for item in dictionary[key]] if dictionary.get(key) is not None else []


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
