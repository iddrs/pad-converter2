import pandas as pd

from pad.converter.parser import ParserBase


class Recurso(ParserBase):
    _file_name = 'RECURSO'
    _spec = (
        ('recurso_vinculado', 1, 4, int),
        ('nome', 5, 84, str),
        ('finalidade', 85, 244, str)
    )

    def __init__(self, logger, sources: list):
        self._logger = logger
        self._sources = sources

    def _prepare(self):
        pass
