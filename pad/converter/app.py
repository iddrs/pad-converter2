"""Classe principal e controller do conversor.
"""
from pad.converter.parser import empenho, liquidac, pagament, balrec

class App:
    _logger = None
    _sources = []
    _writers = []
    cache = 'cache'

    def __init__(self, logger, sources: list, writers: list):
        self._logger = logger
        self._sources = sources
        self._writers = writers


    def run(self):
        self._logger.info('Iniciando o processamento...')
        self._before()
        self._parse()
        self._after()
        self._logger.info('Processamento terminado!')

    def _before(self):
        self._logger.info('Preparando tudo...')
        self._del_cache()


    def _after(self):
        self._logger.info('Executando atividades finais...')
        #mesclara dados dos empenhos com o liquidac e pagament
        #gerar arquivos de restos a pagar


    def _parse(self):
        self._logger.info('Executando a conversão...')
        # df = self._run_parser(empenho.Empenho(self._logger, self._sources))
        # self._write(df, 'empenho')
        # df = self._run_parser(liquidac.Liquidac(self._logger, self._sources))
        # self._write(df, 'liquidac')
        # df = self._run_parser(pagament.Pagament(self._logger, self._sources))
        # self._write(df, 'pagament')
        df = self._run_parser(balrec.BalRec(self._logger, self._sources))
        self._write(df, 'bal_rec')

    def _run_parser(self, parser):
        return parser.parse()


    def _write(self, df, name):
        for w in self._writers:
            w.write(df, name)



    def _del_cache(self):
        self._logger.debug(f'Limpando cache em {self.cache}')
