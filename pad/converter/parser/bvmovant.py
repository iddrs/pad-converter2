import pandas as pd

from pad.converter.parser import ParserBase


class BVMovAnt(ParserBase):
    _file_name = 'BVMOVANT'
    _spec = (
        ('conta_contabil', 1, 20, str),
        ('orgao', 21, 22, int),
        ('uniorcam', 21, 24, int),
        ('movimento_debito_1bim', 25, 37, str),
        ('movimento_credito_1bim', 38, 50, str),
        ('movimento_debito_2bim', 51, 63, str),
        ('movimento_credito_2bim', 64, 76, str),
        ('movimento_debito_3bim', 77, 89, str),
        ('movimento_credito_3bim', 90, 102, str),
        ('movimento_debito_4bim', 103, 115, str),
        ('movimento_credito_4bim', 116, 128, str),
        ('movimento_debito_5bim', 129, 141, str),
        ('movimento_credito_5bim', 142, 154, str),
        ('movimento_debito_6bim', 155, 167, str),
        ('movimento_credito_6bim', 168, 180, str)
    )

    def __init__(self, logger, sources: list):
        self._logger = logger
        self._sources = sources

    def _prepare(self):
        self._df['conta_contabil'] = [el.lstrip('0') for el in self._df['conta_contabil']]
        self._converte_valor('movimento_debito_1bim')
        self._converte_valor('movimento_credito_1bim')
        self._converte_valor('movimento_debito_2bim')
        self._converte_valor('movimento_credito_2bim')
        self._converte_valor('movimento_debito_3bim')
        self._converte_valor('movimento_credito_3bim')
        self._converte_valor('movimento_debito_4bim')
        self._converte_valor('movimento_credito_4bim')
        self._converte_valor('movimento_debito_5bim')
        self._converte_valor('movimento_credito_5bim')
        self._converte_valor('movimento_debito_6bim')
        self._converte_valor('movimento_credito_6bim')

    def _converte_valor(self, campo):
        """Converte o valor em decimal."""
        self._df[campo] = self._df[campo].str.lstrip('0')
        self._df[campo] = pd.to_numeric(self._df[campo], downcast='integer')
        self._df[campo] = round(self._df[campo] / 100, 2)
        self._df[campo] = self._df[campo].fillna(0.0)

