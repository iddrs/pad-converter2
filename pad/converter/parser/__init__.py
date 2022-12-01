"""Módulo base para os parsers
"""
import warnings
from datetime import datetime
from os import path

import pandas as pd


class ParserBase:
    """Calsse base para os parsers.
    """
    _logger = None  # Objeto logger
    _sources = []  # Lista de diretórios de origem dos dados
    _df = None  # pandas.DataFrame com os dados convertidos.
    _cache = 'cache'  # Diretório de cache. Eu sei, ficou estranho pois tem a mesma propriedade em pad.converter.app.App. Vou mudar isso no futuro.

    def parse(self):
        """Controlador da conversão.
        """
        self._logger.info(f'Processando {self._file_name}.txt ...')
        self._text_to_df()
        self._logger.debug(f'Preparando dados de {self._file_name}')
        self._prepare()
        self._inject_entidade()
        self._save_to_cache()
        return self._df


    def _text_to_df(self):
        """Converte os dados de FWF para um pandas.DataFrame.
        """
        self._logger.debug(f'Convertendo texto para data.frame de {self._file_name} ...')
        self._df = []
        for s in self._sources:
            self._logger.debug(f'Lendo {self._file_name} de {s} e convertendo para data.frame...')
            f = path.join(s, f'{self._file_name}.txt')
            if not path.exists(f):
                continue
            with warnings.catch_warnings(): # Ignora um aviso de que não tem converters para todas as colunas, conforme https://docs.python.org/3/library/warnings.html#temporarily-suppressing-warnings
                warnings.simplefilter('ignore')
                df = pd.read_fwf(f, colspecs=self._colspec(), names=self._colnames(), dtype=self._dtypes(), skiprows=1,
                                 skipfooter=1, skipblanklines=True, encoding_errors='replace',
                                 converters=self._converters(),
                                 parse_dates=False,
                                 keep_default_na=True)
                header = self._parse_header(f)
                df = self._inject_header(df, header)
            self._df.append(df)
        self._df = pd.concat(self._df, axis=0, ignore_index=True)


    def _prepare(self):
        """Executa rotinas de preparação.
        """
        raise NotImplementedError('Este método precisa ser implementado pela classe herdeira!')


    def _colspec(self):
        """Lê as especificações de colunas.

        :return Especificações das colunas.
        """
        colspec = []
        for t in self._spec:
            spec = (t[1]-1, t[2])# Para cada coluna, retorna a posição 0-indexed e o limite superior externo para slicing
            colspec.append(spec)
        return colspec

    def _colnames(self):
        """Retorna os nomes das colunas.

        :return Lista com os nomes de colunas.
        """
        colnames = []
        for t in self._spec:
            colnames.append(t[0])
        return colnames

    def _dtypes(self):
        """Retorna os tipos de dados para cada coluna.

        :return Dicionário com os nomes de colunas e o tipo de dados.
        """
        dtypes = {}
        for t in self._spec:
            dtypes[t[0]] = t[3]
        return dtypes

    def _converters(self):
        """Retorna os converters de cada coluna.

        Converters são funções que recebem o valor da coluna e retornam ele com algum processamento.

        :return Lista com os converters das colunas.
        """
        converters = {}
        for t in self._spec:
            if len(t) == 5:
                converters[t[0]] = t[4]
        return converters

    def _inject_header(self, df, header):
        """Concatena os dados do cabeçalho como colunas no data frame.

        :param df pandas.DataFrame
        :param header Dicionário com os dados do cabeçalho.

        :return pandas.DataFrame
        """
        df['cnpj'] = header['cnpj']
        df['data_inicial'] = header['data_inicial']
        df['data_final'] = header['data_final']
        df['data_geracao'] = header['data_geracao']
        return df

    def _parse_header(self, file):
        """Converte o cabeçalho do arquivo em um dicionário de dados.

        :param file Caminho para o arquivo txt de dados.

        :return Dicionário com os dados do cabeçalho.
        """
        with open(file, 'r') as f:
            for l in f:
                h = {
                    'cnpj': l[:14],
                    'data_inicial': datetime.strptime(l[14:22], '%d%m%Y'),
                    'data_final': datetime.strptime(l[22:30], '%d%m%Y'),
                    'data_geracao': datetime.strptime(l[30:38], '%d%m%Y'),
                    'nome_entidade': l[38:]
                }
                break
            return h

    def _inject_entidade(self):
        """Identifica para cada linha de dados, qual entidade ela se refere e adiciona essa informação como uma nova coluna.

        ATENÇÃO: se você estiver usando esse programa, terá que adaptar isso para a sua realidade. Se tentar usar do jeito que está, não terá a informação correta.
        """
        self._df['entidade'] = None # Insere a coluna entidade.
        for i, r in self._df.iterrows():# Para cada linha do data frame
            if self._df.at[i, 'cnpj'] == '12292535000162': # Se houver a coluna cnpj com o valor do CNPJ da câmara.
                self._df.at[i, 'entidade'] = 'cm' # Identifica como da entidade cm
            else: # Se o campo cnpj não tiver o valor da câmara
                if 'orgao' in self._df: # Verifica pelo órgão
                    if self._df.at[i, 'orgao'] == 12: # do RPPS
                        self._df.at[i, 'entidade'] = 'fpsm'
                    else: # ou prefeitura
                        self._df.at[i, 'entidade'] = 'pm'
                elif 'entidade_empenho' in self._df: # verifica pelo campo entidade_empenho
                    if self._df.at[i, 'entidade_empenho'] == 1:
                        self._df.at[i, 'entidade'] = 'fpsm'
                    else:
                        self._df.at[i, 'entidade'] = 'pm'
                elif 'recurso_vinculado' in self._df: # Verifica pelo campo do recurso_vinculado
                    if self._df.at[i, 'recurso_vinculado'] == 50:
                        self._df.at[i, 'entidade'] = 'fpsm'
                    else:
                        self._df.at[i, 'entidade'] = 'pm'
                else: # Se nenhum padrão casar, deixa em branco.
                    self._df.at[i, 'entidade'] = ''

    def _save_to_cache(self):
        """Salva o pandas.DataFrame em cache.
        """
        destiny = path.join(self._cache, f'{self._file_name}.pkl')
        self._logger.debug(f'Salvando {self._file_name} para {destiny}')
        self._df.to_pickle(destiny)
