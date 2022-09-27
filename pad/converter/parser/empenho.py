import pandas as pd

from pad.converter.parser import ParserBase


class Empenho(ParserBase):
    _file_name = 'EMPENHO'
    _spec = (
        ('orgao', 1, 2, int),
        ('uniorcam', 1, 4, int),
        ('funcao', 5, 6, int),
        ('subfuncao', 7, 9, int),
        ('programa', 10, 13, int),
        ('projativ', 17, 21, int),
        ('rubrica', 22, 36, str),
        ('recurso_vinculado', 37, 40, int),
        ('contrapartida_recurso_vinculado', 41, 44, int),
        ('numero_empenho', 45, 57, str),
        ('ano_empenho', 45, 49, int),
        ('entidade_empenho', 50, 51, int),
        ('empenho', 52, 57, int),
        ('data_empenho', 58, 65, str),
        ('valor_empenho', 66, 78, str),
        ('sinal_valor', 79, 79, str),
        ('credor', 80, 89, int),
        ('caracteristica_peculiar_despesa', 255, 257, int),
        ('registro_precos', 260, 260, str),
        ('numero_licitacao', 281, 300, str),
        ('ano_licitacao', 301, 304, int),
        ('historico_empenho', 305, 704, str),
        ('forma_contratacao', 705, 707, str),
        ('base_legal_contratacao', 708, 709, int),
        ('despesa_funcionario', 710, 710, str),
        ('licitacao_compartilhada', 711, 711, str),
        ('cnpj_gerenciador', 712, 725, str),
        ('complemento_recurso_vinculado', 726, 729, int),
        ('indicador_exercicio_fonte_recurso', 730, 730, int),
        ('fonte_recurso', 731, 733, int),
        ('acompanhamento_orcamentario', 734, 737, int)
    )

    def __init__(self, logger, sources: list):
        self._logger = logger
        self._sources = sources

    def _prepare(self):
        self._data_empenho()
        self._valor_empenho()

    def _data_empenho(self):
        """Converte DDMMAAAA para o formato de data do Pandas."""
        self._df['data_empenho'] = pd.to_datetime(self._df['data_empenho'], format='%d%m%Y', exact=True)

    def _valor_empenho(self):
        """Converte o valor do empenho em decimal e remove o sinal."""
        self._df['valor_empenho'] = self._df['sinal_valor'] + self._df['valor_empenho']
        del self._df['sinal_valor']
        self._df['valor_empenho'] = pd.to_numeric(self._df['valor_empenho'], downcast='integer')
        self._df['valor_empenho'] = round(self._df['valor_empenho'] / 100, 2)
