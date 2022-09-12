from pad.converter.parser import ParserBase

class Empenho(ParserBase):
    _file_name = 'EMPENHO'
    _spec = (
        ('orgao', 1, 2, int, len),
        ('uniorcam', 3, 4, int),
        ('funcao', 5, 6, int),
        ('subfuncao', 7, 9, int)
    )

    def __init__(self, logger, sources: list):
        self._logger = logger
        self._sources = sources

    def _prepare(self):
        pass
