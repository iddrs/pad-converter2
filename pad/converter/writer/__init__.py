"""Módulo com os writers.

Um writer nada mais é do que uma classe que salva um pandas.DataFrame em algum outro formato.

É necessário que ela possua um método write que recebe o data frame e um nome.
"""
import csv
from os import path, makedirs

class CsvWriter:
    """Writer para arquivos CSV.
    """
    _logger = None # Objeto logger
    _dir = '' # Diretório onde os arquivos CSV serão salvos.

    def __init__(self, logger, dirname: str) -> None:
        """Construtor do writer

        :param logger: Objeto logger
        :param dirname: Diretório onde os arquivos CSV serão salvos.
        """
        self._logger = logger
        self._dir = dirname
        # Verifica se o diretório existe, se não, cria ele.
        if not path.exists(dirname):
            logger.warn(f'{dirname} não existe e será criado...')
            makedirs(dirname)

    def write(self, df, filename):
        """Salva um pandas.DataFrame para um arquivo CSV.

        :param df pandas.DataFrame
        :param filename Um nome de arquivo sem a extensão.
        """
        destination = path.join(self._dir, f'{filename}.csv')
        self._logger.debug(f'Escrevendo {len(df)} linhas para {destination} ...')
        df.to_csv(destination, sep=';', header=True, index=False, decimal=',', encoding='utf-8', quoting=csv.QUOTE_NONNUMERIC, date_format='%d-%m-%Y', errors='replace')
        self.write_metadata(df, filename)

    def write_metadata(self, df, filename):
        """Salva metadados

        :param df pandas.DataFrame
        :param filename Um nome de arquivo sem a extensão.
        """

        metadata_dir = path.join(self._dir, 'metadata')
        if not path.exists(metadata_dir):
            makedirs(metadata_dir)
        destination = path.join(metadata_dir, f'{filename}.txt')
        self._logger.debug(f'Escrevendo meta dados de {filename} para {destination} ...')
        with open(destination, 'w') as f:
            f.write(str(df.dtypes))
            f.write('\n\r')
            f.write(str(df.head()))


class PickleWriter:
    """Writer para arquivos Pickle.
    """
    _logger = None # Objeto logger
    _dir = '' # Diretório onde os arquivos pickle serão salvos.

    def __init__(self, logger, dirname: str) -> None:
        """Construtor do writer

        :param logger: Objeto logger
        :param dirname: Diretório onde os arquivos pickle serão salvos.
        """
        self._logger = logger
        self._dir = dirname
        # Verifica se o diretório existe, se não, cria ele.
        if not path.exists(dirname):
            logger.warn(f'{dirname} não existe e será criado...')
            makedirs(dirname)

    def write(self, df, filename):
        """Salva um pandas.DataFrame para um arquivo pickle.

        :param df pandas.DataFrame
        :param filename Um nome de arquivo sem a extensão.
        """
        destination = path.join(self._dir, f'{filename}.pickle')
        self._logger.debug(f'Escrevendo {len(df)} linhas para {destination} ...')
        df.to_pickle(destination)
        self.write_metadata(df, filename)

    def write_metadata(self, df, filename):
        """Salva metadados

        :param df pandas.DataFrame
        :param filename Um nome de arquivo sem a extensão.
        """

        metadata_dir = path.join(self._dir, 'metadata')
        if not path.exists(metadata_dir):
            makedirs(metadata_dir)
        destination = path.join(metadata_dir, f'{filename}.txt')
        self._logger.debug(f'Escrevendo meta dados de {filename} para {destination} ...')
        with open(destination, 'w') as f:
            f.write(str(df.dtypes))
            f.write('\n\r')
            f.write(str(df.head()))
