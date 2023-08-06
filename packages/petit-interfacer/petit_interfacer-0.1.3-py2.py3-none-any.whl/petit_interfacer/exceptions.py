

class MissingHints(Exception):
    """The interfacer could'nt find a suitable match for the given prototype and function
    """


class TooManyBlindBinds(Exception):
    """Too many BlindBinds in the given prototype
    """