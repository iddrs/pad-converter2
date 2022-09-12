import csv
from os import path, makedirs

class CsvWriter:
    _logger = None
    _dir = ''

    def __init__(self, logger, dirname: str) -> None:
        self._logger = logger
        self._dir = dirname
        if not path.exists(dirname):
            logger.warn(f'{dirname} não existe e será criado...')
            makedirs(dirname)

    def write(self, df, filename):
        destination = path.join(self._dir, f'{filename}.csv')
        self._logger.debug(f'Escrevendo {len(df)} linhas para {destination} ...')
        df.to_csv(destination, sep=';', header=True, index=False, decimal=',', encoding='utf-8', quoting=csv.QUOTE_NONNUMERIC, date_format='%d-%m-%Y', errors='replace')