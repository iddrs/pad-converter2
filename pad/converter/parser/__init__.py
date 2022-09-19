import pandas as pd
from os import path
import warnings
from datetime import datetime

class ParserBase:
    _logger = None
    _sources = []
    _df = None

    def parse(self):
        self._logger.info(f'Processando {self._file_name}.txt ...')
        self._text_to_df()
        self._logger.debug(f'Preparando dados de {self._file_name}')
        self._prepare()
        return self._df


    def _text_to_df(self):
        self._logger.debug(f'Convertendo texto para data.frame de {self._file_name} ...')
        self._df = []
        for s in self._sources:
            self._logger.debug(f'Lendo {self._file_name} de {s} e convertendo para data.frame...')
            f = path.join(s, f'{self._file_name}.txt')
            if not path.exists(f):
                continue
            with warnings.catch_warnings(): # Ignora um aviso de que não tem converters para todas as colunas, conforme https://docs.python.org/3/library/warnings.html#temporarily-suppressing-warnings
                warnings.simplefilter('ignore')
                df = pd.read_fwf(f, colspecs=self._colspec(), names=self._colnames(), dtype=self._dtypes(), skiprows=1, skipfooter=1, skipblanklines=True, encoding_errors='replace', converters=self._converters())
                header = self._parse_header(f)
                df = self._inject_header(df, header)
            self._df.append(df)
        self._df = pd.concat(self._df, axis=0, ignore_index=True)


    def _prepare(self):
        raise NotImplementedError('Este método precisa ser implementado pela classe herdeira!')


    def _colspec(self):
        colspec = []
        for t in self._spec:
            spec = (t[1]-1, t[2])
            colspec.append(spec)
        return colspec

    def _colnames(self):
        colnames = []
        for t in self._spec:
            colnames.append(t[0])
        return colnames

    def _dtypes(self):
        dtypes = {}
        for t in self._spec:
            dtypes[t[0]] = t[3]
        return dtypes

    def _converters(self):
        converters = {}
        for t in self._spec:
            if len(t) == 5:
                converters[t[0]] = t[4]
        return converters

    def _inject_header(self, df, header):
        df['cnpj'] = header['cnpj']
        df['data_inicial'] = header['data_inicial']
        df['data_final'] = header['data_final']
        df['data_geracao'] = header['data_geracao']
        return df

    def _parse_header(self, file):
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