"""Converte os txt do PAD para CSV
"""

import logging
from os import path
from string import Template

from pad.converter import app, writer

# Configurações

# Local dos arquivos txt do Executivo
pm_input_base_dir_template = Template(r'Z:\Abase\ARQUIVOSPAD\${ano}\MES${mes}')
# Local dos txt do Legislativo
cm_input_base_dir_template = Template(r'Z:\Abase\ARQUIVOSPAD\${ano}\CAMARA\MES${mes}')
# Destino dos arquivos
# output_base_dir = Template(r'C:\Users\Everton\Desktop\Prefeitura\PAD\v2\${ano}-${mes}')
output_base_dir = Template(r'C:\Users\Everton\Desktop\Prefeitura\PAD\${ano}-${mes}')
# Destino dos arquivos para funcionar como um atalho para o mês corrente
# current_base_dir = r'C:\Users\Everton\Desktop\Prefeitura\PAD\v2\current'
current_base_dir = r'C:\Users\Everton\Desktop\Prefeitura\PAD\current'


def main():
    """Ponto de entrada do programa.

    Este é o controller do programa.
    """

    # Configura o logger
    logging.basicConfig(level=logging.NOTSET, format='%(levelname)s:\t\t%(message)s')
    logger = logging

    # Lê o ano e mês a partir da entrada do usuário.
    ano = int(input('Informe o ano desejado [AAAA]: '))
    mes = int(input('Informe o mês desejado [>=1 & <= 12]: '))

    # Verifica se o mês está no intervalo [1,12]
    if (mes < 1) or (mes > 12):
        logger.error(f'O mês {mes} deve estar entre 1 e 12, inclusive.')
        exit(99)
    else:
        mes = str(mes).zfill(2)  # Coloca 0 no início do mês, se for o caso.
    logger.info(f'O período a processar é {mes}/{ano}')

    # Prepara os caminhos de diretório considerando o ano e mês informados pelo usuário.
    pm_input_dir = pm_input_base_dir_template.substitute(ano=ano, mes=mes)
    cm_input_dir = cm_input_base_dir_template.substitute(ano=ano, mes=mes)
    output_dir = output_base_dir.substitute(ano=ano, mes=mes)

    # Carrega os writers, que escreverão dos pandas.DataFrame
    wcsv = writer.CsvWriter(logger, path.join(output_dir, 'csv'))  # CSV writer
    wccsv = writer.CsvWriter(logger, path.join(current_base_dir, 'csv'))  # CSV writer
    wpickle = writer.PickleWriter(logger, path.join(output_dir, 'pickle'))  # Pickle writer
    wcpickle = writer.PickleWriter(logger, path.join(current_base_dir, 'pickle'))  # Pickle writer
    wparquet = writer.ParquetWriter(logger, path.join(output_dir, 'parquet'))  # Parquet writer
    wcparquet = writer.ParquetWriter(logger, path.join(current_base_dir, 'parquet'))  # Parquet writer
    wxlsx = writer.XlsxWriter(logger, path.join(output_dir, 'excel'))  # Xlsx writer
    wcxlsx = writer.XlsxWriter(logger, path.join(current_base_dir, 'excel'))  # Xlsx writer

    # Executa o módulo principal do programa
    running = app.App(logger, [pm_input_dir, cm_input_dir], [wparquet, wcparquet, wxlsx, wcxlsx], mes, ano)
    running.run()


if __name__ == '__main__':
    main()
