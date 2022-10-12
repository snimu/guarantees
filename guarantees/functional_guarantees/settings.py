ACTIVE = True
CACHE = True


def change_settings(active: bool = True, cache: bool = True):
    global ACTIVE, CACHE
    ACTIVE = active
    CACHE = cache

