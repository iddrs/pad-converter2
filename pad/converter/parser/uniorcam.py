import pandas as pd

from pad.converter.parser import ParserBase


class UniOrcam(ParserBase):
    _file_name = 'UNIORCAM'
    _spec = (
        ('exercicio', 1, 4, int),
        ('orgao', 5, 6, int),
        ('uniorcam', 5, 8, int),
        ('nome', 9, 88, str),
        ('identificador', 89, 90, int),
        ('cnpj_uniorcam', 91, 104, str)
    )

    def __init__(self, logger, sources: list):
        self._logger = logger
        self._sources = sources

    def _prepare(self):
        pass
