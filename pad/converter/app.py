"""Classe principal e controller do conversor.
"""
import os.path

import pandas as pd

from pad.converter.parser import empenho, liquidac, pagament, balrec, receita, baldesp, diario, balver, bverenc, rdextra, decreto, brecant, recant, brubant, bver_ant, bvmovant, orgao, uniorcam, programa, projativ, rubrica, recurso, credor, ctadisp, ctaoper

class App:
    _logger = None
    _sources = []
    _writers = []
    _month = 0
    _cache = 'cache'

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
        self._run_writers()
        self._logger.info('Processamento terminado!')

    def _before(self):
        self._logger.info('Preparando tudo...')
        self._del_cache()


    def _after(self):
        self._logger.info('Executando atividades finais...')
        self._liquidac_empenho_concat()
        self._pagament_empenho_concat()


    def _parse(self):
        self._logger.info('Executando a conversão...')
        df = self._run_parser(empenho.Empenho(self._logger, self._sources))
        # self._write(df, 'empenho')
        df = self._run_parser(liquidac.Liquidac(self._logger, self._sources))
        # self._write(df, 'liquidac')
        df = self._run_parser(pagament.Pagament(self._logger, self._sources))
        # self._write(df, 'pagament')
        df = self._run_parser(balrec.BalRec(self._logger, self._sources))
        # self._write(df, 'bal_rec')
        df = self._run_parser(receita.Receita(self._logger, self._sources))
        # self._write(df, 'receita')
        df = self._run_parser(baldesp.BalDesp(self._logger, self._sources))
        # self._write(df, 'bal_desp')
        df = self._run_parser(diario.DiarioContabil(self._logger, self._sources))
        # self._write(df, 'diario_contabil')
        df = self._run_parser(balver.BalVer(self._logger, self._sources))
        # self._write(df, 'bal_ver')
        if self._month == 12:
            df = self._run_parser(bverenc.BVerEnc(self._logger, self._sources))
            # self._write(df, 'bver_enc')
        df = self._run_parser(rdextra.RDExtra(self._logger, self._sources))
        # self._write(df, 'rd_extra')
        # df = self._run_parser(decreto.Decreto(self._logger, self._sources))
        # self._write(df, 'decreto')
        df = self._run_parser(brecant.BRecAnt(self._logger, self._sources))
        # self._write(df, 'brec_ant')
        df = self._run_parser(recant.RecAnt(self._logger, self._sources))
        # self._write(df, 'rec_ant')
        df = self._run_parser(brubant.BRubAnt(self._logger, self._sources))
        # self._write(df, 'brub_ant')
        df = self._run_parser(bver_ant.BVerAnt(self._logger, self._sources))
        # self._write(df, 'bver_ant')
        df = self._run_parser(bvmovant.BVMovAnt(self._logger, self._sources))
        # self._write(df, 'bvmovant')
        df = self._run_parser(orgao.Orgao(self._logger, self._sources))
        # self._write(df, 'orgao')
        df = self._run_parser(uniorcam.UniOrcam(self._logger, self._sources))
        # self._write(df, 'uniorcam')
        df = self._run_parser(programa.Programa(self._logger, self._sources))
        # self._write(df, 'programa')
        df = self._run_parser(projativ.ProjAtiv(self._logger, self._sources))
        # self._write(df, 'projativ')
        df = self._run_parser(rubrica.Rubrica(self._logger, self._sources))
        # self._write(df, 'rubrica')
        df = self._run_parser(recurso.Recurso(self._logger, self._sources))
        # self._write(df, 'recurso')
        df = self._run_parser(credor.Credor(self._logger, self._sources))
        # self._write(df, 'credor')
        df = self._run_parser(ctadisp.CtaDisp(self._logger, self._sources))
        # self._write(df, 'cta_disp')
        df = self._run_parser(ctaoper.CtaOper(self._logger, self._sources))
        # self._write(df, 'cta_oper')

    def _run_parser(self, parser):
        return parser.parse()


    def _write(self, df, name):
        for w in self._writers:
            w.write(df, name)



    def _del_cache(self):
        self._logger.debug(f'Limpando cache em {self._cache}')

    def _liquidac_empenho_concat(self):
        self._logger.debug('Concatenando LIQUIDAC X EMPENHOS...')
        liquidac = pd.read_pickle(os.path.join(self._cache, 'LIQUIDAC.pkl'))
        empenho = pd.read_pickle(os.path.join(self._cache, 'EMPENHO.pkl'))
        empenho.groupby([
            'orgao',
            'uniorcam',
            'funcao',
            'subfuncao',
            'programa',
            'projativ',
            'rubrica',
            'recurso_vinculado',
            'contrapartida_recurso_vinculado',
            'numero_empenho',
            'ano_empenho',
            'entidade_empenho',
            'empenho',
            'credor',
            'caracteristica_peculiar_despesa',
            'registro_precos',
            'numero_licitacao',
            'ano_licitacao',
            'forma_contratacao',
            'base_legal_contratacao',
            'despesa_funcionario',
            'licitacao_compartilhada',
            'cnpj_gerenciador',
            'complemento_recurso_vinculado',
            'indicador_exercicio_fonte_recurso',
            'fonte_recurso',
            'acompanhamento_orcamentario'
        ]).size().reset_index().rename(columns={0: 'contagem'})
        liquidac = pd.merge(liquidac, empenho, on='numero_empenho', how='left')
        liquidac.to_pickle(os.path.join(self._cache, 'LIQUIDAC.pkl'))


    def _pagament_empenho_concat(self):
        self._logger.debug('Concatenando PAGAMENT X EMPENHOS...')
        pagament = pd.read_pickle(os.path.join(self._cache, 'PAGAMENT.pkl'))
        empenho = pd.read_pickle(os.path.join(self._cache, 'EMPENHO.pkl'))
        empenho.groupby([
            'orgao',
            'uniorcam',
            'funcao',
            'subfuncao',
            'programa',
            'projativ',
            'rubrica',
            'recurso_vinculado',
            'contrapartida_recurso_vinculado',
            'numero_empenho',
            'ano_empenho',
            'entidade_empenho',
            'empenho',
            'credor',
            'caracteristica_peculiar_despesa',
            'registro_precos',
            'numero_licitacao',
            'ano_licitacao',
            'forma_contratacao',
            'base_legal_contratacao',
            'despesa_funcionario',
            'licitacao_compartilhada',
            'cnpj_gerenciador',
            'complemento_recurso_vinculado',
            'indicador_exercicio_fonte_recurso',
            'fonte_recurso',
            'acompanhamento_orcamentario'
        ]).size().reset_index().rename(columns={0: 'contagem'})
        pagament = pd.merge(pagament, empenho, on='numero_empenho', how='left')
        pagament.to_pickle(os.path.join(self._cache, 'PAGAMENT.pkl'))

    def _run_writers(self):
        self._logger.info('Escrevendo dados...')
        for f in os.scandir(self._cache):
            if f.is_file():
                df = pd.read_pickle(f.path)
                self._write(df, os.path.splitext(f.name)[0])