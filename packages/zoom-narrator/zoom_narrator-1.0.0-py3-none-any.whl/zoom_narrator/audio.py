import subprocess
from contextlib import AbstractContextManager


def play(path) -> AbstractContextManager:
    return subprocess.Popen(f"ffplay -nodisp -autoexit '{path}'", shell=True)
