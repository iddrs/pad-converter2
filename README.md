# pad-converter2
Conversor de dados gerados para o SIAPC/PAD, agora usando Python

## Qual problema essa aplicação resolve?

Ela converte os dados do formato de campos com largura fixa (*fixed width fields*) para 
outros formatos (atualmente para *CSV*).

Os dados convertidos são os gerados para o envio ao *TCE/RS* por meio do sistema *SIAPC/PAD*.

Além de puramente converter os dados, também são feitos alguns tratamentos e criação de 
medidas (campos calculados).

## Como tudo funciona

A partir da execução de ```convert.py``` ou, preferencialmente, de ```converter.ps1``` 
(que automaticamente ativa e desativa o ambiente virtual *venv*), script solicita o ano 
e o mês desejado e busca os  arquivos no diretório de origem configurado em ```convert.py```.

Após o processamento, os dados resultantes são salvos no destino também configurado em 
```convert.py```.

## Licença

Consulte o arquivo [LICENCE](LICENCE).

## Equipe de desenvolvimento

[Everton da Rosa](https://everton3x.github.io)