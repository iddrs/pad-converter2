class FwfReader:
    _dir = ''

    def __init__(self, path: str) -> None:
        self._dir = path

    def getBaseDir(self) -> str:
        return self._dir