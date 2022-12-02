import pandas as pd

from pad.converter.parser import ParserBase


class Pagament(ParserBase):
    _file_name = 'PAGAMENT'
    _spec = (
        ('numero_empenho', 1, 13, str),
        ('ano_empenho', 1, 5, int),
        ('entidade_empenho', 6, 7, int),
        ('empenho', 8, 13, int),
        ('numero_pagamento', 14, 33, int),
        ('data_pagamento', 34, 41, str),
        ('valor_pagamento', 42, 54, str),
        ('sinal_valor', 55, 55, str),
        ('codigo_operacao', 176, 205, str),
        ('conta_contabil_debito', 206, 225, str),
        ('orgao_debito', 226, 227, int),
        ('uniorcam_debito', 226, 229, int),
        ('conta_contabil_credito', 230, 249, str),
        ('orgao_credito', 250, 251, int),
        ('uniorcam_credito', 250, 253, int),
        ('historico_pagamento', 254, 653, str),
        ('numero_liquidacao', 654, 673, int)
    )

    def __init__(self, logger, sources: list):
        self._logger = logger
        self._sources = sources

    def _prepare(self):
        self._data_pagamento()
        self._valor_pagamento()
        self._df['conta_contabil_debito'] = [el.lstrip('0') for el in self._df['conta_contabil_debito']]
        self._df['conta_contabil_credito'] = [el.lstrip('0') for el in self._df['conta_contabil_credito']]

    def _data_pagamento(self):
        """Converte DDMMAAAA para o formato de data do Pandas."""
        self._df['data_pagamento'] = pd.to_datetime(self._df['data_pagamento'], format='%d%m%Y', exact=True)

    def _valor_pagamento(self):
        """Converte o valor em decimal e remove o sinal."""
        self._df['valor_pagamento'] = self._df['sinal_valor'] + self._df['valor_pagamento']
        del self._df['sinal_valor']
        self._df['valor_pagamento'] = pd.to_numeric(self._df['valor_pagamento'], downcast='integer')
        self._df['valor_pagamento'] = round(self._df['valor_pagamento'] / 100, 2)
