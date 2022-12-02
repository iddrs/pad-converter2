import pandas as pd

from pad.converter.parser import ParserBase


class CtaDisp(ParserBase):
    _file_name = 'CTA_DISP'
    _spec = (
        ('conta_contabil', 1, 20, str),
        ('orgao', 21, 22, int),
        ('uniorcam', 21, 24, int),
        ('recurso_vinculado', 25, 28, int),
        ('banco', 29, 33, int),
        ('agencia', 34, 38, str),
        ('conta_corrente', 39, 58, str),
        ('tipo_conta_corrente', 59, 59, int),
        ('classificacao_disponivel', 60, 60, int),
        ('complemento_recurso_vinculado', 61, 64, int),
        ('indicador_exercicio_fonte_recurso', 65, 65, int),
        ('fonte_recurso', 66, 68, int),
        ('acompanhamento_orcamentario', 69, 72, int)
    )

    def __init__(self, logger, sources: list):
        self._logger = logger
        self._sources = sources

    def _prepare(self):
        self._df['conta_contabil'] = [el.lstrip('0') for el in self._df['conta_contabil']]
