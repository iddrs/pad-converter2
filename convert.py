"""Converte os txt do PAD para CSV
"""

import logging
from string import Template
from os import path

from pad.converter import app, writer

pm_input_base_dir_template = Template(r'.\data_for_test\${ano}\MES${mes}')
cm_input_base_dir_template = Template(r'.\data_for_test\${ano}\CAMARA\MES${mes}')
output_base_dir = Template(r'.\data_for_test\output\${ano}-${mes}')
current_base_dir = r'.\data_for_test\output\current'


def main():
    logging.basicConfig(level=logging.NOTSET, format='%(levelname)s:\t\t%(message)s')
    logger = logging

    ano = input('Informe o ano desejado [AAAA]: ')
    mes = int(input('Informe o mês desejado [>=1 & <= 12]: '))
    if (mes < 1) or (mes > 12):
        logger.error(f'O mês {mes} deve estar entre 1 e 12, inclusive.')
        exit(99)
    else:
        mes = str(mes).zfill(2)
    logger.info(f'O período a processar é {mes}/{ano}')

    pm_input_dir = pm_input_base_dir_template.substitute(ano=ano, mes=mes)
    cm_input_dir = cm_input_base_dir_template.substitute(ano=ano, mes=mes)
    output_dir = output_base_dir.substitute(ano=ano, mes=mes)

    wcsv = writer.CsvWriter(logger, path.join(output_dir, 'csv'))
    wccsv = writer.CsvWriter(logger, path.join(current_base_dir, 'csv'))

    running = app.App(logger, [pm_input_dir, cm_input_dir], [wcsv, wccsv])
    running.run()




if __name__ == '__main__':
    main()
