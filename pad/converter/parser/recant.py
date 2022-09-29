import pandas as pd

from pad.converter.parser import ParserBase


class RecAnt(ParserBase):
    _file_name = 'REC_ANT'
    _spec = (
        ('codigo_receita', 1, 20, str),
        ('orgao', 21, 22, int),
        ('uniorcam', 21, 24, int),
        ('realizada_jan', 25, 37, str),
        ('realizada_fev', 38, 50, str),
        ('realizada_mar', 51, 63, str),
        ('realizada_abr', 64, 76, str),
        ('realizada_mai', 77, 89, str),
        ('realizada_jun', 90, 102, str),
        ('realizada_jul', 103, 115, str),
        ('realizada_ago', 116, 128, str),
        ('realizada_set', 129, 141, str),
        ('realizada_out', 142, 154, str),
        ('realizada_nov', 155, 167, str),
        ('realizada_dez', 168, 180, str),
        ('caracteristica_peculiar_receita', 181, 183, int),
        ('recurso_vinculado', 184, 187, int),
        ('complemento_recurso_vinculado', 188, 191, int),
        ('indicador_exercicio_fonte_recurso', 192, 192, int),
        ('fonte_recurso', 193, 195, int),
        ('codigo_acompanhamento_orcamentario', 196, 199, int)
    )

    def __init__(self, logger, sources: list):
        self._logger = logger
        self._sources = sources

    def _prepare(self):
        self._converte_valor('realizada_jan')
        self._converte_valor('realizada_fev')
        self._converte_valor('realizada_mar')
        self._converte_valor('realizada_abr')
        self._converte_valor('realizada_mai')
        self._converte_valor('realizada_jun')
        self._converte_valor('realizada_jul')
        self._converte_valor('realizada_ago')
        self._converte_valor('realizada_set')
        self._converte_valor('realizada_out')
        self._converte_valor('realizada_nov')
        self._converte_valor('realizada_dez')
        self._receita_realizada()
        self._codigo_receita()
        self._receita_base()
        self._receita_filtro()
        self._classe_receita()
        self._tipo_receita()

    def _receita_realizada(self):
        self._df['receita_realizada'] = round(self._df.loc[:, 'realizada_jan':'realizada_dez'].sum(axis=1), 2)


    def _converte_valor(self, campo):
        """Converte o valor em decimal."""
        self._df[campo] = self._df[campo].str.lstrip('0')
        self._df[campo] = pd.to_numeric(self._df[campo], downcast='integer')
        self._df[campo] = round(self._df[campo] / 100, 2)

    def _codigo_receita(self):
        self._df['codigo_receita'] = self._df['codigo_receita'].str.lstrip('0')

    def _receita_base(self):
        self._df['receita_base'] = ''
        for i, r in self._df.iterrows():
            if self._df.at[i, 'codigo_receita'][:1] == '7':
                self._df.at[i, 'receita_base'] = '1' + self._df.at[i, 'codigo_receita'][1:]
            elif self._df.at[i, 'codigo_receita'][:1] == '8':
                self._df.at[i, 'receita_base'] = '2' + self._df.at[i, 'codigo_receita'][1:]
            elif self._df.at[i, 'codigo_receita'][:1] == '9':
                self._df.at[i, 'receita_base'] = self._df.at[i, 'codigo_receita'][1:]
            else:
                self._df['receita_base'] = self._df['codigo_receita']

    def _receita_filtro(self):
        self._df['filtro'] = self._df['codigo_receita'].str.rstrip('0')
        self._df['filtro_base'] = self._df['receita_base'].str.rstrip('0')

    def _classe_receita(self):
        self._df['classe_receita'] = ''
        for i, r in self._df.iterrows():
            if self._df.at[i, 'codigo_receita'][:1] == '7':
                self._df.at[i, 'classe_receita'] = 'intra'
            elif self._df.at[i, 'codigo_receita'][:1] == '8':
                self._df.at[i, 'classe_receita'] = 'intra'
            elif self._df.at[i, 'codigo_receita'][:1] == '9':
                self._df.at[i, 'classe_receita'] = 'dedutora'
            else:
                self._df['classe_receita'] = 'normal'

    def _tipo_receita(self):
        self._df['tipo_receita'] = ''
        for i, r in self._df.iterrows():
            self._df.at[i, 'tipo_receita'] = self._df.at[i, 'codigo_receita'][7:8]
