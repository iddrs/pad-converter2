"""Converte os txt do PAD para CSV
"""

import logging
from string import Template

from pad.converter import app, reader, writer, specification

pm_input_base_dir_template = Template(r'.\data_for_test\${ano}\MES${mes}')
cm_input_base_dir_template = Template(r'.\data_for_test\${ano}\CAMARA\MES${mes}')
output_base_dir = r'.\data_for_test\output'
current_base_dir = r'.\data_for_test\current'


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
    # logger.info(f'Buscando dados em:\n\t\t-> {pm_input_dir}\n\t\t-> {cm_input_dir}')

    converter = app.App(logger, readers=[reader.FwfReader(pm_input_dir), reader.FwfReader(cm_input_dir)],
              writers=[writer.CsvWriter(output_base_dir), writer.CsvWriter(current_base_dir)], specs=specification.Spec())
    converter.run()


if __name__ == '__main__':
    main()
