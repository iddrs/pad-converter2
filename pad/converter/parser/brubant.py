import pandas as pd

from pad.converter.parser import ParserBase


class BRubAnt(ParserBase):
    _file_name = 'BRUB_ANT'
    _spec = (
        ('orgao', 1, 2, int),
        ('uniorcam', 1, 4, int),
        ('funcao', 5, 6, int),
        ('subfuncao', 7, 9, int),
        ('programa', 10, 13, int),
        ('projativ', 17, 21, int),
        ('rubrica', 22, 36, str),
        ('recurso_vinculado', 37, 40, int),
        ('empenhado_1bim', 41, 51, str),
        ('empenhado_2bim', 52, 62, str),
        ('empenhado_3bim', 63, 73, str),
        ('empenhado_4bim', 74, 84, str),
        ('empenhado_5bim', 85, 95, str),
        ('empenhado_6bim', 96, 106, str),
        ('liquidado_1bim', 107, 117, str),
        ('liquidado_2bim', 118, 128, str),
        ('liquidado_3bim', 129, 139, str),
        ('liquidado_4bim', 140, 150, str),
        ('liquidado_5bim', 151, 161, str),
        ('liquidado_6bim', 162, 172, str),
        ('pago_1bim', 173, 183, str),
        ('pago_2bim', 184, 194, str),
        ('pago_3bim', 195, 205, str),
        ('pago_4bim', 206, 216, str),
        ('pago_5bim', 217, 227, str),
        ('pago_6bim', 228, 238, str),
        ('complemento_recurso_vinculado', 239, 242, int),
        ('indicador_exercicio_fonte_recurso', 243, 243, int),
        ('fonte_recurso', 244, 246, int),
        ('acompanhamento_orcamentario', 247, 250, int)
    )

    def __init__(self, logger, sources: list):
        self._logger = logger
        self._sources = sources

    def _prepare(self):
        # pass
        self._converte_valor('empenhado_1bim')
        self._converte_valor('empenhado_2bim')
        self._converte_valor('empenhado_3bim')
        self._converte_valor('empenhado_4bim')
        self._converte_valor('empenhado_5bim')
        self._converte_valor('empenhado_6bim')
        self._converte_valor('liquidado_1bim')
        self._converte_valor('liquidado_2bim')
        self._converte_valor('liquidado_3bim')
        self._converte_valor('liquidado_4bim')
        self._converte_valor('liquidado_5bim')
        self._converte_valor('liquidado_6bim')
        self._converte_valor('pago_1bim')
        self._converte_valor('pago_2bim')
        self._converte_valor('pago_3bim')
        self._converte_valor('pago_4bim')
        self._converte_valor('pago_5bim')
        self._converte_valor('pago_6bim')
        self._empenhado()
        self._liquidado()
        self._pago()
        self._empenhado_a_liquidar()
        self._empenhado_a_pagar()
        self._liquidado_a_pagar()

    def _converte_valor(self, campo):
        """Converte o valor em decimal."""
        self._df[campo] = self._df[campo].str.lstrip('0')
        self._df[campo] = pd.to_numeric(self._df[campo], downcast='integer')
        self._df[campo] = round(self._df[campo] / 100, 2)
        self._df[campo] = self._df[campo].fillna(0.0)

    def _empenhado(self):
        self._df['valor_empenhado'] = round(self._df.loc[:, 'empenhado_1bim':'empenhado_6bim'].sum(axis=1), 2)

    def _liquidado(self):
        self._df['valor_liquidado'] = round(self._df.loc[:, 'liquidado_1bim':'liquidado_6bim'].sum(axis=1), 2)

    def _pago(self):
        self._df['valor_pago'] = round(self._df.loc[:, 'pago_1bim':'pago_6bim'].sum(axis=1), 2)

    def _empenhado_a_liquidar(self):
        self._df['empenhado_a_liquidar'] = round(
            self._df['valor_empenhado'] - self._df['valor_liquidado'], 2)

    def _empenhado_a_pagar(self):
        self._df['empenhado_a_pagar'] = round(
            self._df['valor_empenhado'] - self._df['valor_pago'], 2)

    def _liquidado_a_pagar(self):
        self._df['liquidado_a_pagar'] = round(
            self._df['valor_liquidado'] - self._df['valor_pago'], 2)
