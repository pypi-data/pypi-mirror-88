#!/usr/bin/env python3

# Standard libraries
from copy import deepcopy
from sys import maxsize

# Modules libraries
from oyaml import dump as yaml_dump

# Components
from ..system.platform import Platform
from ..types.lists import Lists

# JobsFeature class
class JobsFeature:

    # Members
    __configuration = None

    # Constructor
    def __init__(self, jobs, options):

        # Prepare configuration
        self.__configuration = dict()
        if options.names:
            for job in jobs:
                if Lists.match(options.names, job, ignore_case=options.ignore_case,
                               no_regex=options.no_regex):
                    self.__configuration[job] = deepcopy(jobs[job])
                    del self.__configuration[job]['options']
        else:
            for job in jobs:
                self.__configuration[job] = deepcopy(jobs[job])
                del self.__configuration[job]['options']

    # Dump
    def dump(self):

        # Dump configuration results
        print(yaml_dump(self.__configuration, indent=2, width=maxsize))
        print(' ')
        Platform.flush()

        # Result
        return bool(self.__configuration)
