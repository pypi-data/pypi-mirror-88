from .cmd import run


def get_idle_time_sec():
    res = run("xprintidle")
    idle_time_sec = int(res.stdout) / 1000
    return idle_time_sec
