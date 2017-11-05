#!/usr/bin/env python3

"""Colony of ants"""

__author__ = "João Francisco Barreto da Silva Martins"
__email__ = "joaofbsm@dcc.ufmg.br"
__license__ = "GPL"
__version__ = "3.0"

from ant import Ant


class Colony:
    def __init__(self, n):
        """Colony constructor.
        
        Arguments:
            n -- Number of ants in the colony.
        """

        self.ants = []

        for i in range(n):
            self.ants.append(Ant())
    

    def reset_solutions(self):
        """Reset the solution for all the ants in the colony."""
        
        for ant in self.ants:
            ant.reset_solution()
            