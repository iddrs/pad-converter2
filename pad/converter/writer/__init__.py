class CsvWriter:
    _dir = ''

    def __init__(self, path: str) -> None:
        self._dir = path