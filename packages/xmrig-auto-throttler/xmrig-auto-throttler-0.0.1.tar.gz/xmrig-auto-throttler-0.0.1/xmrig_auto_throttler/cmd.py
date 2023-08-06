import subprocess


def run(command, timeout=None):
    return subprocess.run(
        command,
        shell=True,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        universal_newlines=True,
        timeout=timeout,
    )
