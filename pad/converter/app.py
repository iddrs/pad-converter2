"""Classe principal e controller do conversor.
"""

class App:
    _readers = []
    _writers = []
    _specs = None
    logger = None
    cache = 'cache'

    def __init__(self, logger, readers: list, writers: list, specs):
        self._readers = readers
        self._writers = writers
        self._specs = specs
        self.logger = logger


    def run(self):
        self.logger.info('Iniciando o processamento...')
        self._before()
        self._parse()
        self._after()
        self.logger.info('Processamento terminado!')

    def _before(self):
        self.logger.info('Preparando tudo...')
        self.logger.debug(f'Limpando cache em {self.cache}')
        self.logger.debug('Procurando por arquivos em:')
        for r in self._readers:
            d = r.getBaseDir()
            self.logger.debug(d)


    def _after(self):
        self.logger.info('Executando atividades finais...')


    def _parse(self):
        self.logger.info('Executando a conversão...')