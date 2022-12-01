import pandas as pd

from pad.converter.parser import ParserBase


class Decreto(ParserBase):
    _file_name = 'DECRETO'
    _spec = (
        ('nr_lei', 1, 20, str),
        ('data_lei', 21, 28, str),
        ('nr_decreto', 29, 48, str),
        ('data_decreto', 49, 56, str),
        ('valor_credito_adicional', 57, 69, str),
        ('valor_reducao_dotacoes', 70, 82, str),
        ('tipo_credito_adicional', 83, 83, int),
        ('origem_recurso', 84, 84, int),
        ('alteracao_orcamentaria', 85, 85, int),
        ('valor_alteracao_orcamentaria', 86, 98, str),
        ('data_reabertura', 99, 106, str),
        ('valor_reaberto', 107, 119, str),
        ('recurso_vinculado_suplementacao', 41, 44, str),
        ('recurso_vinculado_reducao', 41, 44, str),
        ('indicador_exercicio_fonte_recurso_suplementacao', 128, 128, int),
        ('fonte_recurso_suplementacao', 129, 131, int),
        ('indicador_exercicio_fonte_recurso_reducao', 132, 132, int),
        ('fonte_recurso_reducao', 133, 135, int)
    )

    def __init__(self, logger, sources: list):
        self._logger = logger
        self._sources = sources

    def _prepare(self):
        # pass
        self._converte_valor('valor_credito_adicional')
        self._converte_valor('valor_reducao_dotacoes')
        self._converte_valor('valor_alteracao_orcamentaria')
        self._converte_valor('valor_reaberto')
        self._converte_data('data_lei')
        self._converte_data('data_decreto')
        self._converte_data('data_reabertura')


    def _converte_valor(self, campo):
        """Converte o valor em decimal."""
        self._df[campo] = self._df[campo].str.lstrip('0')
        self._df[campo] = pd.to_numeric(self._df[campo], downcast='integer')
        self._df[campo] = round(self._df[campo] / 100, 2)
        self._df[campo] = self._df[campo].fillna(0.0)

    def _converte_data(self, campo):
        """Converte DDMMAAAA para o formato de data do Pandas."""
        self._df[campo] = pd.to_datetime(self._df[campo], format='%d%m%Y', exact=True, errors='ignore')
