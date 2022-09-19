import pandas as pd

from pad.converter.parser import ParserBase


class Liquidac(ParserBase):
    _file_name = 'LIQUIDAC'
    _spec = (
        ('numero_empenho', 1, 13, str),
        ('ano_empenho', 1, 5, int),
        ('entidade_empenho', 6, 7, int),
        ('empenho', 8, 13, int),
        ('numero_liquidacao', 14, 33, int),
        ('data_liquidacao', 34, 41, str),
        ('valor_liquidacao', 42, 54, str),
        ('sinal_valor', 55, 55, str),
        ('codigo_operacao', 221, 250, str),
        ('historico_liquidacao', 251, 650, str),
        ('existe_contrato', 651, 651, str),
        ('numero_contrato_tce', 652, 671, int),
        ('numero_contrato', 671, 691, str),
        ('ano_contrato', 692, 695, int),
        ('existe_documento_fiscal', 696, 696, str),
        ('numero_documento_fiscal', 697, 705, int),
        ('serie_documento_fiscal', 706, 708, str),
        ('tipo_instrumento_contratual', 709, 709, str)
    )

    def __init__(self, logger, sources: list):
        self._logger = logger
        self._sources = sources

    def _prepare(self):
        self._data_liquidacao()
        self._valor_liquidacao()

    def _data_liquidacao(self):
        """Converte DDMMAAAA para o formato de data do Pandas."""
        self._df['data_liquidacao'] = pd.to_datetime(self._df['data_liquidacao'], format='%d%m%Y', exact=True)

    def _valor_liquidacao(self):
        """Converte o valor em decimal e remove o sinal."""
        self._df['valor_liquidacao'] = self._df['sinal_valor'] + self._df['valor_liquidacao']
        del self._df['sinal_valor']
        self._df['valor_liquidacao'] = pd.to_numeric(self._df['valor_liquidacao'], downcast='integer')
        self._df['valor_liquidacao'] = round(self._df['valor_liquidacao'] / 100, 2)
