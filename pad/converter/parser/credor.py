import pandas as pd

from pad.converter.parser import ParserBase


class Credor(ParserBase):
    _file_name = 'CREDOR'
    _spec = (
        ('credor', 1, 10, int),
        ('nome', 11, 70, str),
        ('cnpj_cpf', 71, 84, str),
        ('inscricao_estadual', 85, 99, int),
        ('inscricao_municipal', 100, 114, int),
        ('endereco', 115, 164, str),
        ('cidade', 165, 194, str),
        ('uf', 195, 196, str),
        ('cep', 197, 204, int),
        ('telefone', 205, 219, int),
        ('fax', 220, 234, int),
        ('tipo_credor', 235, 236, int),
        ('tipo_pessoa', 237, 238, int)
    )

    def __init__(self, logger, sources: list):
        self._logger = logger
        self._sources = sources

    def _prepare(self):
        self._cpf_cnpj_split()


    def _cpf_cnpj_split(self):
        self._df['cpf_credor'] = None
        self._df['cnpj_credor'] = None
        self._df.astype({'cpf_credor': str, 'cnpj_credor': str})
        for i, r in self._df.iterrows():
            if r['tipo_pessoa'] == 1:
                self._df.at[i, 'cpf_credor'] = r['cnpj_cpf']
            elif r['tipo_pessoa'] == 2:
                self._df.at[i, 'cnpj_credor'] = r['cnpj_cpf']
            else:
                pass
        del self._df['cnpj_cpf']