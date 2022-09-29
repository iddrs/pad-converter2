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
        pass
