import pandas as pd

from pad.converter.parser import ParserBase


class Rubrica(ParserBase):
    _file_name = 'RUBRICA'
    _spec = (
        ('exercicio', 1, 4, int),
        ('rubrica', 5, 19, str),
        ('especificacao', 20, 129, str),
        ('tipo_nivel', 130, 130, str),
        ('numero_nivel', 131, 132, int)
    )

    def __init__(self, logger, sources: list):
        self._logger = logger
        self._sources = sources

    def _prepare(self):
        pass
