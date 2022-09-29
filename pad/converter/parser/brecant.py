import pandas as pd

from pad.converter.parser import ParserBase


class BRecAnt(ParserBase):
    _file_name = 'BREC_ANT'
    _spec = (
        ('codigo_receita', 1, 20, str),
        ('orgao', 21, 22, int),
        ('uniorcam', 21, 24, int),
        ('receita_orcada', 25, 37, str),
        ('receita_realizada', 38, 50, str),
        ('recurso_vinculado', 51, 54, int),
        ('especificacao_receita', 55, 224, str),
        ('tipo_nivel_receita', 225, 225, str),
        ('numero_nivel_receita', 226, 227, int),
        ('caracteristica_peculiar_receita', 228, 230, int),
        ('complemento_recurso_vinculado', 231, 234, int),
        ('indicador_exercicio_fonte_recurso', 235, 235, int),
        ('fonte_recurso', 236, 238, int),
        ('codigo_acompanhamento_orcamentario', 239, 242, int)
    )

    def __init__(self, logger, sources: list):
        self._logger = logger
        self._sources = sources

    def _prepare(self):
        self._receita_orcada()
        self._receita_realizada()
        self._previsto_arrecadado()
        self._codigo_receita()
        self._receita_base()
        self._receita_filtro()
        self._classe_receita()
        self._tipo_receita()

    def _receita_orcada(self):
        self._converte_valor('receita_orcada')

    def _receita_realizada(self):
        self._converte_valor('receita_realizada')

    def _previsto_arrecadado(self):
        self._df['excesso_frustracao'] = round(self._df['receita_realizada'] - self._df['receita_orcada'], 2)

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
