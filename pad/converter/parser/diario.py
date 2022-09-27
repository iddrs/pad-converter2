import pandas as pd

from pad.converter.parser import ParserBase


class DiarioContabil(ParserBase):
    _file_name = 'tce_4111'
    _spec = (
        ('conta_contabil', 1, 20, str),
        ('orgao', 21, 22, int),
        ('uniorcam', 21, 24, int),
        ('nr_lancamento', 29, 40, int),
        ('nr_lote', 41, 52, int),
        ('nr_documento', 53, 65, int),
        ('data_lancamento', 66, 73, str),
        ('valor', 74, 90, str),
        ('tipo_lancamento', 91, 91, str),
        ('nr_arquivamento', 92, 103,int),
        ('historico', 104, 253, str),
        ('tipo_documento', 254, 254, str),
        ('natureza_informacao', 255, 255, str),
        ('indicador_superavit_financeiro', 256, 256, str),
        ('recurso_vinculado', 257, 260, int),
        ('complemento_recurso_vinculado', 261, 264, int),
        ('indicador_exercicio_fonte_recurso', 265, 265, int),
        ('fonte_recurso', 266, 268, int),
        ('acompanhamento_orcamentario', 269, 272, int)
    )

    def __init__(self, logger, sources: list):
        self._logger = logger
        self._sources = sources

    def _prepare(self):
        # pass
        self._converte_valor('valor')
        self._data_lancamento()

    def _converte_valor(self, campo):
        """Converte o valor em decimal."""
        self._df[campo] = self._df[campo].str.lstrip('0')
        self._df[campo] = pd.to_numeric(self._df[campo], downcast='integer')
        self._df[campo] = round(self._df[campo] / 100, 2)
        self._df[campo] = self._df[campo].fillna(0.0)

    def _data_lancamento(self):
        """Converte DDMMAAAA para o formato de data do Pandas."""
        self._df['data_lancamento'] = pd.to_datetime(self._df['data_lancamento'], format='%d%m%Y', exact=True)