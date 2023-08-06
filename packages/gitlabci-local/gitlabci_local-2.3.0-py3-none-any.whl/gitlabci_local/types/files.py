#!/usr/bin/env python3

# Standard libraries
from atexit import register
from pathlib import Path
from signal import SIGINT, signal, SIGTERM
from tempfile import NamedTemporaryFile

# Files class
class Files:

    # Members
    registered = False
    temps = []

    # Clean
    @staticmethod
    def clean():

        # Delete all temps
        for temp in Files.temps:
            temp_file = Path(temp.name)
            if temp_file.exists():
                temp_file.unlink()

        # Reset temps
        Files.temps = []

    # Temp
    @staticmethod
    def temp(path=None, mode='wt', newline='\n', prefix='.tmp.'):

        # Create temporary file
        temp_file = NamedTemporaryFile(delete=False, dir=path, mode=mode, newline=newline,
                                       prefix=prefix)

        # Register temporary file
        Files.temps += [temp_file]

        # Register cleanup
        if not Files.registered:
            register(Files.clean)
            signal(SIGINT, Files.clean)
            signal(SIGTERM, Files.clean)
            Files.registered = True

        # Result
        return temp_file
