import pandas as pd

from pad.converter.parser import ParserBase


class Receita(ParserBase):
    _file_name = 'RECEITA'
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
        ('meta_1bim', 181, 192, str),
        ('meta_2bim', 193, 204, str),
        ('meta_3bim', 205, 216, str),
        ('meta_4bim', 217, 228, str),
        ('meta_5bim', 229, 240, str),
        ('meta_6bim', 241, 252, str),
        ('caracteristica_peculiar_receita', 253, 255, int),
        # ('recurso_vinculado', 256, 259, int), #removido a partir de jan/2023
        # ('complemento_recurso_vinculado', 260, 263, int), #removido a partir de jan/2023
        ('indicador_exercicio_fonte_recurso', 264, 264, int),
        ('fonte_recurso', 265, 267, int),
        ('codigo_acompanhamento_orcamentario', 268, 271, int)
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
        self._converte_valor('meta_1bim')
        self._converte_valor('meta_2bim')
        self._converte_valor('meta_3bim')
        self._converte_valor('meta_4bim')
        self._converte_valor('meta_5bim')
        self._converte_valor('meta_6bim')
        self._meta_total()
        self._receita_realizada()
        self._receita_a_arrecadar()
        self._codigo_receita()
        self._receita_base()
        self._receita_filtro()
        self._classe_receita()
        self._tipo_receita()
        self._metas_mensais()

    def _meta_total(self):
        self._df['meta_total'] = round(self._df.loc[:, 'meta_1bim':'meta_6bim'].sum(axis=1), 2)

    def _receita_realizada(self):
        self._df['receita_realizada'] = round(self._df.loc[:, 'realizada_jan':'realizada_dez'].sum(axis=1), 2)

    def _receita_a_arrecadar(self):
        self._df['meta_a_arrecadar'] = round(self._df['meta_total'] - self._df['receita_realizada'], 2)


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
            t = int(self._df.at[i, 'receita_base'][7:8])
            if (t == 0) and (self._df.at[
                                 i, 'fonte_recurso'] > 0):  # Considera como principal, mesmo que o tipo_receita seja 0, porque tem receitas que foram cadastradas com 0 em vez de 1
                t = 1
            self._df.at[i, 'tipo_receita'] = t

    def _metas_mensais(self):
        self._df['meta_jan'] = 0.0
        self._df['meta_fev'] = 0.0
        self._df['meta_mar'] = 0.0
        self._df['meta_abr'] = 0.0
        self._df['meta_mai'] = 0.0
        self._df['meta_jun'] = 0.0
        self._df['meta_jul'] = 0.0
        self._df['meta_ago'] = 0.0
        self._df['meta_set'] = 0.0
        self._df['meta_out'] = 0.0
        self._df['meta_nov'] = 0.0
        self._df['meta_dez'] = 0.0
        for i, r in self._df.iterrows():
            m1b = round(r['meta_1bim']/2, 2)
            m2b = round(r['meta_2bim'] / 2, 2)
            m3b = round(r['meta_3bim'] / 2, 2)
            m4b = round(r['meta_4bim'] / 2, 2)
            m5b = round(r['meta_5bim'] / 2, 2)
            m6b = round(r['meta_6bim'] / 2, 2)
            self._df.at[i, 'meta_jan'] = m1b
            self._df.at[i, 'meta_fev'] = round(r['meta_1bim'] - m1b, 2)
            self._df.at[i, 'meta_mar'] = m2b
            self._df.at[i, 'meta_abr'] = round(r['meta_2bim'] - m2b, 2)
            self._df.at[i, 'meta_mai'] = m3b
            self._df.at[i, 'meta_jun'] = round(r['meta_3bim'] - m3b, 2)
            self._df.at[i, 'meta_jul'] = m4b
            self._df.at[i, 'meta_ago'] = round(r['meta_4bim'] - m4b, 2)
            self._df.at[i, 'meta_set'] = m5b
            self._df.at[i, 'meta_out'] = round(r['meta_5bim'] - m5b, 2)
            self._df.at[i, 'meta_nov'] = m6b
            self._df.at[i, 'meta_dez'] = round(r['meta_6bim'] - m6b, 2)
