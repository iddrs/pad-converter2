"""Módulo principal do conversor.
"""

import os.path
from datetime import datetime
import pandas as pd
from pad.converter.parser import empenho, liquidac, pagament, balrec, receita, baldesp, diario, balver, bverenc, \
    rdextra, decreto, brecant, recant, brubant, bver_ant, bvmovant, orgao, uniorcam, programa, projativ, rubrica, recurso, \
    credor, ctadisp, ctaoper



class App:
    """Classe principal do programa.
    """
    _logger = None # Objeto logger
    _sources = [] # Lista de diretórios de origem dos dados
    _writers = [] # Lista de objetos writer
    _month = 0 # Mês em processamento
    _year = 0 # Ano em processamento
    _cache = 'cache' # Diretório de cache para o processamento

    def __init__(self, logger, sources: list, writers: list, month: int, year: int):
        """Construtor da classe principal.

        :param logger Objeto logger.
        :param sources Lista de diretórios de origem dos dados.
        :param writers Lista com instâncias dos writers
        :param month Mês que será processado
        :param year Ano que será processado
        """
        self._logger = logger
        self._sources = sources
        self._writers = writers
        self._month = month
        self._year = year


    def run(self):
        """Executa a rotina principal da conversão.
        """
        self._logger.info('Iniciando o processamento...')
        self._before() # Executa ações preparatórias.
        self._parse() # Executa a conversão propriamente dita.
        self._after() # Executa rotinas de finalização.
        self._run_writers() # Executa os writers
        self._logger.info('Processamento terminado!')

    def _before(self):
        """Controlador de rotinas preparatórias.

        As rotinas preparatórias envolvem limpeza de cache e quaisquer outras que se façam necessárias à preparação para a conversão.
        """
        self._logger.info('Preparando tudo...')
        self._del_cache()

    def _after(self):
        """Controlador de rotinas de finalização.

        As rotinas de finalização englobam quaisquer processamentos extras que precisem ser feitos somente com todos os arquivos já convertidos e outras rotinas pós-conversão.
        """
        self._logger.info('Executando atividades finais...')
        self._liquidac_empenho_concat()
        self._pagament_empenho_concat()
        self._restos_pagar()
        self._moviemp()

    def _parse(self):
        """Controlador da conversão.
        """
        self._logger.info('Executando a conversão...')
        # Aqui eu optei por uma certa repetição de código para cada arquivo a ser convertido, pois, é possível que,
        # no futuro, algum arquivo necessite de alguma rotina mais específica.
        # Como não se espera grandes mudanças em termos de arquivos a processar, penso que seja uma solução adequada.
        # Entretanto, talvez eu refatore isso no futuro fazendo um loop numa lista de parsers.
        df = self._run_parser(empenho.Empenho(self._logger, self._sources))
        df = self._run_parser(liquidac.Liquidac(self._logger, self._sources))
        df = self._run_parser(pagament.Pagament(self._logger, self._sources))
        df = self._run_parser(balrec.BalRec(self._logger, self._sources))
        df = self._run_parser(receita.Receita(self._logger, self._sources))
        df = self._run_parser(baldesp.BalDesp(self._logger, self._sources))
        df = self._run_parser(diario.DiarioContabil(self._logger, self._sources))
        df = self._run_parser(balver.BalVer(self._logger, self._sources))
        if self._month == '12': # O arquivo BVER_ENC somente é gerado no mês 12
            df = self._run_parser(bverenc.BVerEnc(self._logger, self._sources))
        df = self._run_parser(rdextra.RDExtra(self._logger, self._sources))
        df = self._run_parser(decreto.Decreto(self._logger, self._sources))
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
        """Executa um parser específico.

        :param parser Instância de pad.converter.parser.ParserBase

        :return pandas.DataFrame
        """
        return parser.parse()

    def _write(self, df, name):
        """Executa os writers.

        :param df pandas.DataFrame
        :param name Nome do arquivo/tabela para salvar os dados.
        """
        for w in self._writers:
            w.write(df, name)

    def _del_cache(self):
        """Apaga os arquivos em cache.
        """
        self._logger.debug(f'Limpando cache em {self._cache}')

    def _liquidac_empenho_concat(self):
        """Concatena os dados de cada liquidação com os respectivos empenhos.
        """
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
                           'codigo_acompanhamento_orcamentario']]
        empenho = empenho.drop_duplicates()
        liquidac = pd.merge(liquidac, empenho, on='numero_empenho', how='left', suffixes=('', '_r'))
        liquidac.to_pickle(os.path.join(self._cache, 'LIQUIDAC.pkl'))

    def _pagament_empenho_concat(self):
        """Concatena os dados de cada pagamento com os respectivos empenhos.
        """
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
            'codigo_acompanhamento_orcamentario'
        ]]
        empenho = empenho.drop_duplicates()
        pagament = pd.merge(pagament, empenho, on='numero_empenho', how='left', suffixes=('', '_r'))
        pagament.to_pickle(os.path.join(self._cache, 'PAGAMENT.pkl'))

    def _run_writers(self):
        """Controlador da escrita dos dados.
        """
        self._logger.info('Escrevendo dados...')
        for f in os.scandir(self._cache):
            if f.is_file():
                df = pd.read_pickle(f.path)
                self._write(df, os.path.splitext(f.name)[0])

    def _restos_pagar(self):
        """Cria um arquivo com os saldos e movimentações de empenhos inscritos em restos a pagar.
        """
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
            'codigo_acompanhamento_orcamentario'
        ]]

        restos = restos.drop_duplicates()
        restos = restos[restos['ano_empenho'] < int(self._year)]

        restos['saldo_inicial_nao_processados'] = 0.0
        restos['cancelamento_nao_processados'] = 0.0
        restos['liquidacao_nao_processados'] = 0.0
        restos['a_liquidar_nao_processados'] = 0.0
        restos['pagamento_nao_processados'] = 0.0
        restos['liquidado_a_pagar_nao_processados'] = 0.0
        restos['cancelamento_nao_processados_liquidados'] = 0.0
        restos['saldo_final_nao_processados'] = 0.0
        restos['saldo_inicial_processados'] = 0.0
        restos['cancelamento_processados'] = 0.0
        restos['pagamento_processados'] = 0.0
        restos['saldo_final_processados'] = 0.0
        restos['saldo_inicial_nao_processados_inscritos_ultimo_ano'] = 0.0
        restos['saldo_inicial_nao_processados_inscritos_anos_anteriores'] = 0.0
        restos['saldo_inicial_processados_inscritos_ultimo_ano'] = 0.0
        restos['saldo_inicial_processados_inscritos_anos_anteriores'] = 0.0
        restos['entidade'] = None
        data_corte = datetime(int(self._year), 1, 1)
        for i, r in restos.iterrows():
            if r['orgao'] == 1:
                restos.at[i, 'entidade'] = 'cm'
            elif r['orgao'] == 12:
                restos.at[i, 'entidade'] = 'fpsm'
            else:
                restos.at[i, 'entidade'] = 'pm'

            restos.at[i, 'saldo_inicial_nao_processados'] = self._saldo_inicial_nao_processados(r['numero_empenho'],
                                                                                                empenho, liquidac,
                                                                                                data_corte)
            restos.at[i, 'cancelamento_nao_processados'] = self._cancelamento_nao_processados(r['numero_empenho'],
                                                                                              empenho, data_corte,
                                                                                              self._year)
            restos.at[i, 'liquidacao_nao_processados'] = self._liquidacao_nao_processados(r['numero_empenho'], liquidac,
                                                                                          data_corte, self._year)
            restos.at[i, 'a_liquidar_nao_processados'] = round(
                restos.at[i, 'saldo_inicial_nao_processados'] - restos.at[i, 'cancelamento_nao_processados'] -
                restos.at[i, 'liquidacao_nao_processados'], 2)
            if restos.at[i, 'saldo_inicial_nao_processados'] > 0.0:
                restos.at[i, 'pagamento_nao_processados'] = self._pagamento_nao_processados(r['numero_empenho'],
                                                                                            pagament, data_corte,
                                                                                            self._year)
            restos.at[i, 'liquidado_a_pagar_nao_processados'] = round(
                restos.at[i, 'liquidacao_nao_processados'] - restos.at[i, 'pagamento_nao_processados'], 2)
            restos.at[i, 'saldo_final_nao_processados'] = round(
                restos.at[i, 'saldo_inicial_nao_processados'] - restos.at[i, 'cancelamento_nao_processados'] -
                restos.at[i, 'pagamento_nao_processados'], 2)
            restos.at[i, 'saldo_inicial_processados'] = self._saldo_inicial_processados(r['numero_empenho'], liquidac,
                                                                                        pagament, data_corte)
            restos.at[i, 'cancelamento_processados'] = self._cancelamento_processados(r['numero_empenho'], liquidac,
                                                                                      data_corte, self._year)
            if restos.at[i, 'saldo_inicial_processados'] > 0.0:
                restos.at[i, 'pagamento_processados'] = self._pagamento_processados(r['numero_empenho'], pagament,
                                                                                    data_corte, self._year)
            restos.at[i, 'saldo_final_processados'] = round(
                restos.at[i, 'saldo_inicial_processados'] - restos.at[i, 'cancelamento_processados'] - restos.at[
                    i, 'pagamento_processados'], 2)
            if r['ano_empenho'] == (int(self._year) - 1):
                restos.at[
                    i, 'saldo_inicial_nao_processados_inscritos_ultimo_ano'] = self._saldo_inicial_nao_processados(
                    r['numero_empenho'], empenho, liquidac, data_corte)
                restos.at[i, 'saldo_inicial_processados_inscritos_ultimo_ano'] = self._saldo_inicial_processados(
                    r['numero_empenho'], liquidac, pagament, data_corte)
            else:
                restos.at[
                    i, 'saldo_inicial_nao_processados_inscritos_anos_anteriores'] = self._saldo_inicial_nao_processados(
                    r['numero_empenho'], empenho, liquidac, data_corte)
                restos.at[i, 'saldo_inicial_processados_inscritos_anos_anteriores'] = self._saldo_inicial_processados(
                    r['numero_empenho'], liquidac, pagament, data_corte)

        restos = self._ajusta_cancelamento_restos(restos)

        restos.to_pickle(os.path.join(self._cache, 'RESTOS_PAGAR.pkl'))

    def _ajusta_cancelamento_restos(self, restos):
        for i, r in restos.iterrows():
            if restos.at[i, 'cancelamento_processados'] > restos.at[i, 'saldo_final_nao_processados']:
                diff = restos.at[i, 'cancelamento_processados'] - restos.at[i, 'saldo_final_nao_processados'];
                # restos.at[i, 'cancelamento_nao_processados'] += diff
                restos.at[i, 'cancelamento_processados'] -= diff
                restos.at[i, 'cancelamento_nao_processados_liquidados'] = diff
                # restos.at[i, 'saldo_final_nao_processados'] -= diff
                restos.at[i, 'saldo_final_processados'] += diff
        return restos

    def _pagamento_processados(self, numero_empenho, pagament, data_corte, ano):
        """Método auxiliar para _restos_pagar
        """
        valor_pago = pagament[
            (pagament.numero_empenho == numero_empenho) & (pagament['data_pagamento'] >= data_corte) & (
                        pagament.ano_empenho < int(ano))]['valor_pagamento'].sum()
        return round(valor_pago, 2)

    def _cancelamento_processados(self, numero_empenho, liquidac, data_corte, ano):
        """Método auxiliar para _restos_pagar
        """
        valor_cancelado = liquidac[
            (liquidac.numero_empenho == numero_empenho) & (liquidac['data_liquidacao'] >= data_corte) & (
                        liquidac.valor_liquidacao < 0.0) & (liquidac.ano_empenho < int(ano))]['valor_liquidacao'].sum()
        return round(valor_cancelado * -1, 2)

    def _saldo_inicial_processados(self, numero_empenho, liquidac, pagament, data_corte):
        """Método auxiliar para _restos_pagar
        """
        valor_liquidacao = \
        liquidac[(liquidac.numero_empenho == numero_empenho) & (liquidac['data_liquidacao'] < data_corte)][
            'valor_liquidacao'].sum()
        valor_pago = pagament[(pagament.numero_empenho == numero_empenho) & (pagament['data_pagamento'] < data_corte)][
            'valor_pagamento'].sum()
        saldo = valor_liquidacao - valor_pago
        return round(saldo, 2)

    def _pagamento_nao_processados(self, numero_empenho, pagament, data_corte, ano):
        """Método auxiliar para _restos_pagar
        """
        valor_pago = pagament[
            (pagament.numero_empenho == numero_empenho) & (pagament['data_pagamento'] >= data_corte) & (
                        pagament.ano_empenho < int(ano))]['valor_pagamento'].sum()
        return round(valor_pago, 2)

    def _liquidacao_nao_processados(self, numero_empenho, liquidac, data_corte, ano):
        """Método auxiliar para _restos_pagar
        """
        valor_liquidado = liquidac[
            (liquidac.numero_empenho == numero_empenho) & (liquidac['data_liquidacao'] >= data_corte) & (
                        liquidac.ano_empenho < int(ano))]['valor_liquidacao'].sum()
        return round(valor_liquidado, 2)

    def _saldo_inicial_nao_processados(self, numero_empenho, empenho, liquidac, data_corte):
        """Método auxiliar para _restos_pagar
        """
        valor_empenho = empenho[(empenho.numero_empenho == numero_empenho) & (empenho['data_empenho'] < data_corte)][
            'valor_empenho'].sum()
        valor_liquidacao = \
        liquidac[(liquidac.numero_empenho == numero_empenho) & (liquidac['data_liquidacao'] < data_corte)][
            'valor_liquidacao'].sum()
        saldo = valor_empenho - valor_liquidacao
        return round(saldo, 2)

    def _cancelamento_nao_processados(self, numero_empenho, empenho, data_corte, ano):
        """Método auxiliar para _restos_pagar
        """
        valor_cancelado = empenho[
            (empenho.numero_empenho == numero_empenho) & (empenho['data_empenho'] >= data_corte) & (
                        empenho.valor_empenho < 0.0) & (empenho.ano_empenho < int(ano))]['valor_empenho'].sum()
        return round(valor_cancelado * -1, 2)

    def _moviemp(self):
        """Cria um arquivo com os saldos e movimentações de empenhos do ano.
        """
        self._logger.debug('Montando MOVIEMP...')
        liquidac = pd.read_pickle(os.path.join(self._cache, 'LIQUIDAC.pkl'))
        pagament = pd.read_pickle(os.path.join(self._cache, 'PAGAMENT.pkl'))
        empenho = pd.read_pickle(os.path.join(self._cache, 'EMPENHO.pkl'))
        moviemp = empenho[[
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
            'codigo_acompanhamento_orcamentario'
        ]]

        moviemp = moviemp.drop_duplicates()
        moviemp = moviemp[moviemp['ano_empenho'] == int(self._year)]

        moviemp['empenhado_bruto'] = 0.0
        moviemp['estorno_empenhado'] = 0.0
        moviemp['empenhado_liquido'] = 0.0
        moviemp['liquidacao_bruto'] = 0.0
        moviemp['estorno_liquidacao'] = 0.0
        moviemp['liquidacao_liquido'] = 0.0
        moviemp['pagamento_bruto'] = 0.0
        moviemp['estorno_pagamento'] = 0.0
        moviemp['pagamento_liquido'] = 0.0
        moviemp['empenhado_a_liquidar'] = 0.0
        moviemp['empenhado_a_pagar'] = 0.0
        moviemp['liquidacao_a_pagar'] = 0.0
        moviemp['entidade'] = None
        data_corte = datetime(int(self._year), 1, 1)
        for i, r in moviemp.iterrows():
            if r['orgao'] == 1:
                moviemp.at[i, 'entidade'] = 'cm'
            elif r['orgao'] == 12:
                moviemp.at[i, 'entidade'] = 'fpsm'
            else:
                moviemp.at[i, 'entidade'] = 'pm'

            moviemp.at[i, 'empenhado_bruto'] = self._empenhado_bruto(r['numero_empenho'], empenho, data_corte)
            moviemp.at[i, 'estorno_empenhado'] = self._estorno_empenhado(r['numero_empenho'], empenho, data_corte)
            moviemp.at[i, 'empenhado_liquido'] = round(moviemp.at[i, 'empenhado_bruto'] - moviemp.at[i, 'estorno_empenhado'], 2)

            moviemp.at[i, 'liquidacao_bruto'] = self._liquidacao_bruto(r['numero_empenho'], liquidac, data_corte)
            moviemp.at[i, 'estorno_liquidacao'] = self._estorno_liquidacao(r['numero_empenho'], liquidac, data_corte)
            moviemp.at[i, 'liquidacao_liquido'] = round(moviemp.at[i, 'liquidacao_bruto'] - moviemp.at[i, 'estorno_liquidacao'], 2)

            moviemp.at[i, 'pagamento_bruto'] = self._pagamento_bruto(r['numero_empenho'], pagament, data_corte)
            moviemp.at[i, 'estorno_pagamento'] = self._estorno_pagamento(r['numero_empenho'], pagament, data_corte)
            moviemp.at[i, 'pagamento_liquido'] = round(moviemp.at[i, 'pagamento_bruto'] - moviemp.at[i, 'estorno_pagamento'], 2)

            moviemp.at[i, 'empenhado_a_liquidar'] = round(
                moviemp.at[i, 'empenhado_liquido'] - moviemp.at[i, 'liquidacao_liquido'], 2)
            moviemp.at[i, 'empenhado_a_pagar'] = round(
                moviemp.at[i, 'empenhado_liquido'] - moviemp.at[i, 'pagamento_liquido'], 2)
            moviemp.at[i, 'liquidacao_a_pagar'] = round(
                moviemp.at[i, 'liquidacao_liquido'] - moviemp.at[i, 'pagamento_liquido'], 2)

        moviemp.to_pickle(os.path.join(self._cache, 'MOVIEMP.pkl'))


    def _empenhado_bruto(self, numero_empenho, empenho, data_corte):
        """Método auxiliar para _moviemp
        """
        valor = empenho[
            (empenho.numero_empenho == numero_empenho) & (empenho['data_empenho'] >= data_corte) & (
                        empenho.valor_empenho > 0.0)]['valor_empenho'].sum()
        return round(valor, 2)

    def _estorno_empenhado(self, numero_empenho, empenho, data_corte):
        """Método auxiliar para _moviemp
        """
        valor = empenho[
            (empenho.numero_empenho == numero_empenho) & (empenho['data_empenho'] >= data_corte) & (
                        empenho.valor_empenho < 0.0)]['valor_empenho'].sum()
        return round(valor * -1, 2)

    def _liquidacao_bruto(self, numero_empenho, liquidac, data_corte):
        """Método auxiliar para _moviemp
        """
        valor = liquidac[
            (liquidac.numero_empenho == numero_empenho) & (liquidac['data_liquidacao'] >= data_corte) & (
                    liquidac.valor_liquidacao > 0.0)]['valor_liquidacao'].sum()
        return round(valor, 2)

    def _estorno_liquidacao(self, numero_empenho, liquidac, data_corte):
        """Método auxiliar para _moviemp
        """
        valor = liquidac[
            (liquidac.numero_empenho == numero_empenho) & (liquidac['data_liquidacao'] >= data_corte) & (
                    liquidac.valor_liquidacao < 0.0)]['valor_liquidacao'].sum()
        return round(valor * -1, 2)

    def _pagamento_bruto(self, numero_empenho, pagament, data_corte):
        """Método auxiliar para _moviemp
        """
        valor = pagament[
            (pagament.numero_empenho == numero_empenho) & (pagament['data_pagamento'] >= data_corte) & (
                    pagament.valor_pagamento > 0.0)]['valor_pagamento'].sum()
        return round(valor, 2)

    def _estorno_pagamento(self, numero_empenho, pagament, data_corte):
        """Método auxiliar para _moviemp
        """
        valor = pagament[
            (pagament.numero_empenho == numero_empenho) & (pagament['data_pagamento'] >= data_corte) & (
                    pagament.valor_pagamento < 0.0)]['valor_pagamento'].sum()
        return round(valor * -1, 2)