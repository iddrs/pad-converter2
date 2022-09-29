"""Classe principal e controller do conversor.
"""
from pad.converter.parser import empenho, liquidac, pagament, balrec, receita, baldesp, diario, balver, bverenc, rdextra, decreto, brecant, recant, brubant, bver_ant, bvmovant

class App:
    _logger = None
    _sources = []
    _writers = []
    cache = 'cache'
    _month = 0

    def __init__(self, logger, sources: list, writers: list, month: int):
        self._logger = logger
        self._sources = sources
        self._writers = writers
        self._month = month


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
        # df = self._run_parser(balrec.BalRec(self._logger, self._sources))
        # self._write(df, 'bal_rec')
        # df = self._run_parser(receita.Receita(self._logger, self._sources))
        # self._write(df, 'receita')
        # df = self._run_parser(baldesp.BalDesp(self._logger, self._sources))
        # self._write(df, 'bal_desp')
        # df = self._run_parser(diario.DiarioContabil(self._logger, self._sources))
        # self._write(df, 'diario_contabil')
        # df = self._run_parser(balver.BalVer(self._logger, self._sources))
        # self._write(df, 'bal_ver')
        # if self._month == 12:
        #     df = self._run_parser(bverenc.BVerEnc(self._logger, self._sources))
        #     self._write(df, 'bver_enc')
        # df = self._run_parser(rdextra.RDExtra(self._logger, self._sources))
        # self._write(df, 'rd_extra')
        # df = self._run_parser(decreto.Decreto(self._logger, self._sources))
        # self._write(df, 'decreto')
        # df = self._run_parser(brecant.BRecAnt(self._logger, self._sources))
        # self._write(df, 'brec_ant')
        # df = self._run_parser(recant.RecAnt(self._logger, self._sources))
        # self._write(df, 'rec_ant')
        # df = self._run_parser(brubant.BRubAnt(self._logger, self._sources))
        # self._write(df, 'brub_ant')
        # df = self._run_parser(bver_ant.BVerAnt(self._logger, self._sources))
        # self._write(df, 'bver_ant')
        df = self._run_parser(bvmovant.BVMovAnt(self._logger, self._sources))
        self._write(df, 'bvmovant')

    def _run_parser(self, parser):
        return parser.parse()


    def _write(self, df, name):
        for w in self._writers:
            w.write(df, name)



    def _del_cache(self):
        self._logger.debug(f'Limpando cache em {self.cache}')
