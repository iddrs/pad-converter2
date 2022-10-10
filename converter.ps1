$hello = @"
#################################################################
# PROGRAMA PARA CONVERTER OS TXT DO SIAPC/PAD                   #
#                                                               #
# Este programa converte os dados FWF gerados para o            #
# SIAPC/PAD para outros formatos.                               #
#                                                               #
# Desenvolvido por Everton da Rosa<https://everton3x.github.io> #
# Para licenciamento e detalhes, consulte:                      #
# https://github.com/iddrs/pad-converter2                       #
#################################################################
"@

# Inicia o venv
.\venv\Scripts\activate.ps1

# Executa a conversão
python convert.py

# desativa o venv
deactivate