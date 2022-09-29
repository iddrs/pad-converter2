import pandas as pd

from pad.converter.parser import ParserBase


class Programa(ParserBase):
    _file_name = 'PROGRAMA'
    _spec = (
        ('exercicio', 1, 4, int),
        ('programa', 5, 8, int),
        ('nome', 9, 86, str)
    )

    def __init__(self, logger, sources: list):
        self._logger = logger
        self._sources = sources

    def _prepare(self):
        pass
