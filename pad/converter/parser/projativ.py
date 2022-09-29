import pandas as pd

from pad.converter.parser import ParserBase


class ProjAtiv(ParserBase):
    _file_name = 'PROJATIV'
    _spec = (
        ('exercicio', 1, 4, int),
        ('projativ', 5, 9, int),
        ('nome', 10, 89, str),
        ('identificador', 90, 91, int)
    )

    def __init__(self, logger, sources: list):
        self._logger = logger
        self._sources = sources

    def _prepare(self):
        pass
