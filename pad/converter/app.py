"""Classe principal e controller do conversor.
"""
import os.path

import pandas as pd

from datetime import datetime

from pad.converter.parser import empenho, liquidac, pagament, balrec, receita, baldesp, diario, balver, bverenc, rdextra, decreto, brecant, recant, brubant, bver_ant, bvmovant, orgao, uniorcam, programa, projativ, rubrica, recurso, credor, ctadisp, ctaoper

class App:
    _logger = None
    _sources = []
    _writers = []
    _month = 0
    _year = 0
    _cache = 'cache'

    def __init__(self, logger, sources: list, writers: list, month: int, year: int):
        self._logger = logger
        self._sources = sources
        self._writers = writers
        self._month = month
        self._year = year


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
        self._restos_pagar()


    def _parse(self):
        self._logger.info('Executando a conversão...')
        df = self._run_parser(empenho.Empenho(self._logger, self._sources))
        df = self._run_parser(liquidac.Liquidac(self._logger, self._sources))
        df = self._run_parser(pagament.Pagament(self._logger, self._sources))
        df = self._run_parser(balrec.BalRec(self._logger, self._sources))
        df = self._run_parser(receita.Receita(self._logger, self._sources))
        df = self._run_parser(baldesp.BalDesp(self._logger, self._sources))
        df = self._run_parser(diario.DiarioContabil(self._logger, self._sources))
        df = self._run_parser(balver.BalVer(self._logger, self._sources))
        if self._month == 12:
            df = self._run_parser(bverenc.BVerEnc(self._logger, self._sources))
        df = self._run_parser(rdextra.RDExtra(self._logger, self._sources))
        # df = self._run_parser(decreto.Decreto(self._logger, self._sources))
        df = self._run_parser(brecant.BRecAnt(self._logger, self._sources))
        df = self._run_parser(recant.RecAnt(self._logger, self._sources))
        df = self._run_parser(brubant.BRubAnt(self._logger, self._sources))
        df = self._run_parser(bver_ant.BVerAnt(self._logger, self._sources))
        df = self._run_parser(bvmovant.BVMovAnt(self._logger, self._sources))
        df = self._run_parser(orgao.Orgao(self._logger, self._sources))
        df = self._run_parser(uniorcam.UniOrcam(self._logger, self._sources))
        df = self._run_parser(programa.Programa(self._logger, self._sources))
        df = self._run_parser(projativ.ProjAtiv(self._logger, self._sources))
        df = self._run_parser(rubrica.Rubrica(self._logger, self._sources))
        df = self._run_parser(recurso.Recurso(self._logger, self._sources))
        df = self._run_parser(credor.Credor(self._logger, self._sources))
        df = self._run_parser(ctadisp.CtaDisp(self._logger, self._sources))
        df = self._run_parser(ctaoper.CtaOper(self._logger, self._sources))

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
        empenho = empenho[['orgao',
            'uniorcam',
            'funcao',
            'subfuncao',
            'programa',
            'projativ',
            'rubrica',
            'recurso_vinculado',
            'contrapartida_recurso_vinculado',
            'numero_empenho',
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
            'acompanhamento_orcamentario']]
        empenho = empenho.drop_duplicates()
        liquidac = pd.merge(liquidac, empenho, on='numero_empenho', how='left', suffixes=('', '_r'))
        liquidac.to_pickle(os.path.join(self._cache, 'LIQUIDAC.pkl'))


    def _pagament_empenho_concat(self):
        self._logger.debug('Concatenando PAGAMENT X EMPENHOS...')
        pagament = pd.read_pickle(os.path.join(self._cache, 'PAGAMENT.pkl'))
        empenho = pd.read_pickle(os.path.join(self._cache, 'EMPENHO.pkl'))
        empenho = empenho[[
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
        ]]
        empenho = empenho.drop_duplicates()
        pagament = pd.merge(pagament, empenho, on='numero_empenho', how='left', suffixes=('', '_r'))
        pagament.to_pickle(os.path.join(self._cache, 'PAGAMENT.pkl'))

    def _run_writers(self):
        self._logger.info('Escrevendo dados...')
        for f in os.scandir(self._cache):
            if f.is_file():
                df = pd.read_pickle(f.path)
                self._write(df, os.path.splitext(f.name)[0])

    def _restos_pagar(self):
        self._logger.debug('Montando RESTOS_PAGAR...')
        liquidac = pd.read_pickle(os.path.join(self._cache, 'LIQUIDAC.pkl'))
        pagament = pd.read_pickle(os.path.join(self._cache, 'PAGAMENT.pkl'))
        empenho = pd.read_pickle(os.path.join(self._cache, 'EMPENHO.pkl'))
        restos = empenho[[
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
        ]]

        restos = restos.drop_duplicates()
        restos = restos[restos['ano_empenho'] <= int(self._year)]

        restos['saldo_inicial_nao_processados'] = 0.0
        restos['cancelamento_nao_processados'] = 0.0
        restos['liquidacao_nao_processados'] = 0.0
        restos['a_liquidar_nao_processados'] = 0.0
        restos['pagamento_nao_processados'] = 0.0
        restos['liquidado_a_pagar_nao_processados'] = 0.0
        restos['saldo_final_nao_processados'] = 0.0
        restos['saldo_inicial_processados'] = 0.0
        restos['cancelamento_processados'] = 0.0
        empenho['pagamento_processados'] = 0.0
        restos['saldo_final_processados'] = 0.0
        data_corte = datetime(int(self._year), 1, 1)
        for i, r in restos.iterrows():
            restos.at[i, 'saldo_inicial_nao_processados'] = self._saldo_inicial_nao_processados(r['numero_empenho'], empenho, liquidac, data_corte)
            restos.at[i, 'cancelamento_nao_processados'] = self._cancelamento_nao_processados(r['numero_empenho'], empenho, data_corte, self._year)
            restos.at[i, 'liquidacao_nao_processados'] = self._liquidacao_nao_processados(r['numero_empenho'], liquidac, data_corte, self._year)
            restos.at[i, 'a_liquidar_nao_processados'] = round(restos.at[i, 'saldo_inicial_nao_processados'] - restos.at[i, 'cancelamento_nao_processados'] - restos.at[i, 'liquidacao_nao_processados'], 2)
            if restos.at[i, 'saldo_inicial_nao_processados'] > 0.0:
                restos.at[i, 'pagamento_nao_processados'] = self._pagamento_nao_processados(r['numero_empenho'], pagament, data_corte, self._year)
            restos.at[i, 'liquidado_a_pagar_nao_processados'] = round(restos.at[i, 'liquidacao_nao_processados'] - restos.at[i, 'pagamento_nao_processados'], 2)
            restos.at[i, 'saldo_final_nao_processados'] = round(restos.at[i, 'saldo_inicial_nao_processados'] - restos.at[i, 'cancelamento_nao_processados'] - restos.at[i, 'pagamento_nao_processados'], 2)


        restos.to_pickle(os.path.join(self._cache, 'RESTOS_PAGAR.pkl'))

    def _pagamento_nao_processados(self, numero_empenho, pagament, data_corte, ano):
        valor_pago = pagament[(pagament.numero_empenho == numero_empenho) & (pagament['data_pagamento'] >= data_corte) & (pagament.ano_empenho < int(ano))]['valor_pagamento'].sum()
        return round(valor_pago, 2)

    def _liquidacao_nao_processados(self, numero_empenho, liquidac, data_corte, ano):
        valor_liquidado = liquidac[(liquidac.numero_empenho == numero_empenho) & (liquidac['data_liquidacao'] >= data_corte) & (liquidac.ano_empenho < int(ano))]['valor_liquidacao'].sum()
        return round(valor_liquidado, 2)

    def _saldo_inicial_nao_processados(self, numero_empenho, empenho, liquidac, data_corte):
        valor_empenho = empenho[(empenho.numero_empenho == numero_empenho) & (empenho['data_empenho'] < data_corte)]['valor_empenho'].sum()
        valor_liquidacao = liquidac[(liquidac.numero_empenho == numero_empenho) & (liquidac['data_liquidacao'] < data_corte)]['valor_liquidacao'].sum()
        saldo = valor_empenho - valor_liquidacao
        return round(saldo, 2)

    def _cancelamento_nao_processados(self, numero_empenho, empenho, data_corte, ano):
        valor_cancelado = empenho[(empenho.numero_empenho == numero_empenho) & (empenho['data_empenho'] >= data_corte) & (empenho.valor_empenho < 0.0) & (empenho.ano_empenho < int(ano))]['valor_empenho'].sum()
        return round(valor_cancelado * -1, 2)

