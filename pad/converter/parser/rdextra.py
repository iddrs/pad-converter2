import pandas as pd

from pad.converter.parser import ParserBase


class RDExtra(ParserBase):
    _file_name = 'RD_EXTRA'
    _spec = (
        ('conta_contabil', 1, 20, str),
        ('orgao', 21, 22, int),
        ('uniorcam', 21, 24, int),
        ('valor_movimento', 25, 37, str),
        ('identificador_ingresso_dispendio', 38, 38, str),
        ('classificacao', 39, 40, int),
        # ('recurso_vinculado', 41, 44, int) removido a partir de jan/2023
    )

    def __init__(self, logger, sources: list):
        self._logger = logger
        self._sources = sources

    def _prepare(self):
        self._df['conta_contabil'] = [el.lstrip('0') for el in self._df['conta_contabil']]
        self._converte_valor('valor_movimento')


    def _converte_valor(self, campo):
        """Converte o valor em decimal."""
        self._df[campo] = self._df[campo].str.lstrip('0')
        self._df[campo] = pd.to_numeric(self._df[campo], downcast='integer')
        self._df[campo] = round(self._df[campo] / 100, 2)
        self._df[campo] = self._df[campo].fillna(0.0)
