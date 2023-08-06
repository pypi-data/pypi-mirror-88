import logging
import sys

from .cmd import run

logger = logging.getLogger()


def has_dependency(program: str) -> bool:
    """Uses which to check if a cli program is installed.
    Returns True if program exists, False otherwise.

    Note: This will not work on Windows

    Args:
        program (str): the program to check for

    Returns:
        bool
    """
    res = run(f"which {program}")
    return res.returncode == 0


def check_dependencies():
    if sys.platform == "linux" and not has_dependency("xprintidle"):
        logger.info("you have to install xprintidle first")
        sys.exit(1)
