import pandas as pd

from pad.converter.parser import ParserBase


class Orgao(ParserBase):
    _file_name = 'ORGAO'
    _spec = (
        ('exercicio', 1, 4, int),
        ('orgao', 5, 6, int),
        ('nome', 7, 86, str)
    )

    def __init__(self, logger, sources: list):
        self._logger = logger
        self._sources = sources

    def _prepare(self):
        pass
