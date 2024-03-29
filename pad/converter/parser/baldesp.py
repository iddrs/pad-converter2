import pandas as pd

from pad.converter.parser import ParserBase


class BalDesp(ParserBase):
    _file_name = 'BAL_DESP'
    _spec = (
        ('orgao', 1, 2, int),
        ('uniorcam', 1, 4, int),
        ('funcao', 5, 6, int),
        ('subfuncao', 7, 9, int),
        ('programa', 10, 13, int),
        ('projativ', 17, 21, int),
        ('elemento', 22, 27, str),
        # ('recurso_vinculado', 28, 31, int), #removido a partir de jan/2023
        ('dotacao_inicial', 32, 44, str),
        ('atualizacao_monetaria', 45, 57, str),
        ('credito_suplementar', 58, 70, str),
        ('credito_especial', 71, 83, str),
        ('credito_extraordinario', 84, 96, str),
        ('reducao_dotacao', 97, 109, str),
        # ('suplementacao_recurso_vinculado', 110, 122, str), #removido a partir de jan/2023
        # ('reducao_recurso_vinculado', 123, 135, str), #removido a partir de jan/2023
        ('valor_empenhado', 136, 148, str),
        ('valor_liquidado', 149, 161, str),
        ('valor_pago', 162, 174, str),
        ('valor_limitado', 175, 187, str),
        ('valor_recomposto', 188, 200, str),
        ('previsao_realizacao', 201, 213, str),
        # ('complemento_recurso_vinculado', 214, 217, int), #removido a partir de jan/2023
        ('transferencia', 218, 230, str),
        ('transposicao', 231, 243, str),
        ('remanejamento', 244, 256, str),
        ('indicador_exercicio_fonte_recurso', 257, 257, int),
        ('fonte_recurso', 258, 260, int),
        # ('acompanhamento_orcamentario', 261, 264, int) #removido a partir de jan/2023
    )

    def __init__(self, logger, sources: list):
        self._logger = logger
        self._sources = sources

    def _prepare(self):
        # pass
        self._converte_valor('dotacao_inicial')
        self._converte_valor('atualizacao_monetaria')
        self._converte_valor('credito_suplementar')
        self._converte_valor('credito_especial')
        self._converte_valor('credito_extraordinario')
        self._converte_valor('reducao_dotacao')
        # self._converte_valor('suplementacao_recurso_vinculado') removido a partir de jan/2023
        # self._converte_valor('reducao_recurso_vinculado') removido a partir de jan/2023
        self._converte_valor('valor_empenhado')
        self._converte_valor('valor_liquidado')
        self._converte_valor('valor_pago')
        self._converte_valor('valor_limitado')
        self._converte_valor('valor_recomposto')
        self._converte_valor('previsao_realizacao')
        self._converte_valor('transferencia')
        self._converte_valor('transposicao')
        self._converte_valor('remanejamento')
        self._dotacao_atualizada()
        self._credito_adicional()
        self._dotacao_a_empenhar()
        self._empenhado_a_liquidar()
        self._empenhado_a_pagar()
        self._liquidado_a_pagar()

    def _converte_valor(self, campo):
        """Converte o valor em decimal."""
        self._df[campo] = self._df[campo].str.lstrip('0')
        self._df[campo] = pd.to_numeric(self._df[campo], downcast='integer')
        self._df[campo] = round(self._df[campo] / 100, 2)
        self._df[campo] = self._df[campo].fillna(0.0)

    def _dotacao_atualizada(self):
        self._df['dotacao_atualizada'] = round(
            self._df['dotacao_inicial'].fillna(0.0) + self._df['atualizacao_monetaria'].fillna(0.0) + self._df['credito_suplementar'].fillna(0.0) +
            self._df['credito_especial'].fillna(0.0) + self._df[
                'credito_extraordinario'].fillna(0.0) - self._df['reducao_dotacao'].fillna(0.0) + self._df['transferencia'].fillna(0.0) + self._df['transposicao'].fillna(0.0) + self._df[
                'remanejamento'].fillna(0.0), 2)

    def _credito_adicional(self):
        self._df['credito_adicional'] = round(
            self._df['dotacao_atualizada'].fillna(0.0) - self._df['dotacao_inicial'].fillna(0.0), 2)

    def _dotacao_a_empenhar(self):
        self._df['dotacao_a_empenhar'] = round(
            self._df['dotacao_atualizada'].fillna(0.0) - self._df['valor_empenhado'].fillna(0.0), 2)

    def _empenhado_a_liquidar(self):
        self._df['empenhado_a_liquidar'] = round(
            self._df['valor_empenhado'].fillna(0.0) - self._df['valor_liquidado'].fillna(0.0), 2)

    def _empenhado_a_pagar(self):
        self._df['empenhado_a_pagar'] = round(
            self._df['valor_empenhado'].fillna(0.0) - self._df['valor_pago'].fillna(0.0), 2)

    def _liquidado_a_pagar(self):
        self._df['liquidado_a_pagar'] = round(
            self._df['valor_liquidado'].fillna(0.0) - self._df['valor_pago'].fillna(0.0), 2)
