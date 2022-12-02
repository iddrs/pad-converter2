import pandas as pd

from pad.converter.parser import ParserBase


class CtaOper(ParserBase):
    _file_name = 'CTA_OPER'
    _spec = (
        ('operacao', 1, 30, str),
        ('data', 31, 38, str),
        ('valor', 39, 51, str),
        ('sinal_valor', 25, 52, str),
        ('recurso_vinculado', 53, 56, int),
        ('codigo_receita', 57, 76, str),
        ('orgao_receita', 77, 78, int),
        ('uniorcam_receita', 77, 80, int),
        ('conta_contabil', 81, 100, str),
        ('orgao_conta_contabil', 101, 102, int),
        ('uniorcam_conta_contabil', 101, 104, int),
        ('complemento_recurso_vinculado', 105, 108, int),
        ('indicador_exercicio_fonte_recurso', 109, 109, int),
        ('fonte_recurso', 109, 112, int),
        ('acompanhamento_orcamentario', 113, 116, int)
    )

    def __init__(self, logger, sources: list):
        self._logger = logger
        self._sources = sources

    def _prepare(self):
        self._df['conta_contabil'] = [el.lstrip('0') for el in self._df['conta_contabil']]
        self._data()
        self._valor()


    def _data(self):
        """Converte DDMMAAAA para o formato de data do Pandas."""
        self._df['data'] = pd.to_datetime(self._df['data'], format='%d%m%Y', exact=True)

    def _valor(self):
        """Converte o valor do empenho em decimal e remove o sinal."""
        self._df['valor'] = self._df['sinal_valor'] + self._df['valor']
        del self._df['sinal_valor']
        self._df['valor'] = pd.to_numeric(self._df['valor'], downcast='integer')
        self._df['valor'] = round(self._df['valor'] / 100, 2)