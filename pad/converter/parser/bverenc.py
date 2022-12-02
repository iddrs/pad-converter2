import pandas as pd

from pad.converter.parser import ParserBase


class BVerEnc(ParserBase):
    _file_name = 'BVER_ENC'
    _spec = (
        ('conta_contabil', 1, 20, str),
        ('orgao', 21, 22, int),
        ('uniorcam', 21, 24, int),
        ('saldo_anterior_devedor', 25, 37, str),
        ('saldo_anterior_credor', 38, 50, str),
        ('movimento_devedor', 51, 63, str),
        ('movimento_credor', 64, 76, str),
        ('saldo_atual_devedor', 77, 89, str),
        ('saldo_atual_credor', 90, 102, str),
        ('especificacao_conta', 103, 250, str),
        ('tipo_nivel_conta', 251, 251, str),
        ('nr_nivel_conta', 252, 253, int),
        ('escrituracao', 255, 255, str),
        ('natureza_informacao', 256, 256, str),
        ('indicador_superavit_financeiro', 257, 257, str),
        ('recurso_vinculado', 258, 261, int),
        ('complemento_recurso_vinculado', 262, 265, int),
        ('indicador_exercicio_fonte_recurso', 266, 266, int),
        ('fonte_recurso', 267, 269, int),
        ('acompanhamento_orcamentario', 270, 273, int)
    )

    def __init__(self, logger, sources: list):
        self._logger = logger
        self._sources = sources

    def _prepare(self):
        # pass
        self._converte_valor('saldo_anterior_devedor')
        self._converte_valor('saldo_anterior_credor')
        self._converte_valor('movimento_devedor')
        self._converte_valor('movimento_credor')
        self._converte_valor('saldo_atual_devedor')
        self._converte_valor('saldo_atual_credor')
        self._consolida_saldo_anterior()
        self._consolida_saldo_atual()
        self._df['conta_contabil'] = [el.lstrip('0') for el in self._df['conta_contabil']]

    def _converte_valor(self, campo):
        """Converte o valor em decimal."""
        self._df[campo] = self._df[campo].str.lstrip('0')
        self._df[campo] = pd.to_numeric(self._df[campo], downcast='integer')
        self._df[campo] = round(self._df[campo] / 100, 2)
        self._df[campo] = self._df[campo].fillna(0.0)

    def _consolida_saldo_anterior(self):
        self._df['valor_saldo_inicial'] = 0.0
        self._df['natureza_saldo_inicial'] = ''
        for i, r in self._df.iterrows():
            classe = r['conta_contabil'][0:1]
            sd = r['saldo_anterior_devedor']
            sc = r['saldo_anterior_credor']
            if classe == '1' or classe == '3' or classe == '5' or classe == '7':
                saldo = round(sd - sc, 2)
                if saldo > 0:
                    natureza = 'D'
                elif saldo < 0:
                    natureza = 'C'
                    saldo = abs(saldo)
                else:
                    natureza = ''
            else:
                saldo = round(sc - sd, 2)
                if saldo > 0:
                    natureza = 'C'
                elif saldo < 0:
                    natureza = 'D'
                    saldo = abs(saldo)
                else:
                    natureza = ''

            self._df.at[i, 'valor_saldo_inicial'] = saldo
            self._df.at[i, 'natureza_saldo_inicial'] = natureza

    def _consolida_saldo_atual(self):
        self._df['valor_saldo_final'] = 0.0
        self._df['natureza_saldo_final'] = ''
        for i, r in self._df.iterrows():
            classe = r['conta_contabil'][0:1]
            sd = r['saldo_atual_devedor']
            sc = r['saldo_atual_credor']
            if classe == '1' or classe == '3' or classe == '5' or classe == '7':
                saldo = round(sd - sc, 2)
                if saldo > 0:
                    natureza = 'D'
                elif saldo < 0:
                    natureza = 'C'
                    saldo = abs(saldo)
                else:
                    natureza = ''
            else:
                saldo = round(sc - sd, 2)
                if saldo > 0:
                    natureza = 'C'
                elif saldo < 0:
                    natureza = 'D'
                    saldo = abs(saldo)
                else:
                    natureza = ''

            self._df.at[i, 'valor_saldo_final'] = saldo
            self._df.at[i, 'natureza_saldo_final'] = natureza