import os
from socket import timeout
import urllib.request
import requests
import datetime
import eventlet
import uploadS3 as upds3

# verifica se a pasta arquivosPMC existe e, se não, cria a mesma
if os.path.exists('arquivosPMC') == False:
    os.mkdir('arquivosPMC')

# verifica se a pasta ultimoImportado existe e, se não, cria a mesma
if os.path.exists('ultimoImportado') == False:
    os.mkdir('ultimoImportado')    

# verifica se o arquivo ultimoImportado.txt existe e, se não, cria o mesmo
if os.path.exists('ultimoImportado/ultimoImportado.txt') == False:
    arquivo = open('ultimoImportado/ultimoImportado.txt','w')
    arquivo.write("vazio")
    arquivo.close

# lê o arquivo ultimoImportado.txt para pegar o último arquivo baixado
arquivo = open('ultimoImportado/ultimoImportado.txt','r')
for linha in arquivo:
    linha = linha.rstrip()
arquivo.close()

# verifica se o arquivo ultimoImportado.txt tem a informação do último arquivo.xls baixado
if linha == 'vazio':
    url = 'https://ftp.ibge.gov.br/Comercio_e_Servicos/Pesquisa_Mensal_de_Comercio/Tabelas/2018/pmc_201801_00.xls'   
else:
    url = linha

ultimaURL = ''
seq = url[96:98]

ano=url[80:84]
anomes= url[89:95]

while True: # loop infinito que procura até 12 sequências de arquivos dentro de cada mês
    seq= int(seq) + 1
    seq = '%02d' % seq

    url = url[:80] + str(ano) + url[84:89] + str(anomes) + '_' + str(seq) + url[98:102]

    print('+++++ verifica url - ' + str(datetime.datetime.now()))
    print(url)
    response = requests.get(url, verify=False, timeout=None)

    if int(seq) < 13: # procura até 12 sequências do arquivo dentro do mês

        if response.status_code == 200: # vê se url existe
            #print('Web site exists')
            print('..... baixa arquivo - ' + str(datetime.datetime.now()))
            with eventlet.Timeout(None):
                urllib.request.urlretrieve(url, 'arquivosPMC/' + url[85:102])

            print('..... arquivo baixado - ' + str(datetime.datetime.now()))
            upds3.upload_fileS3('arquivosPMC/' + url[85:102], 'arquivosPMCs3', 'aws_access_key', 'aws_secret_key')
            ultimaURL = url

    else: # passa para o próximo mês e verifica se quebrou o ano
        #print('Web site does not exist')

        seq = 0
        anomes = int(anomes) + 1
        anocorrente = datetime.date.today().year
        anomesStr = str(anomes)

        if int(anomesStr[4:6]) > 12:
            if int(anocorrente) > int(ano):
                ano = int(ano) + 1
                anomes = str(ano) + '01'
            else:
                break

if len(ultimaURL) > 0: # grava a posição do último arquivo pmc.xls baixado
    arquivo = open('ultimoImportado/ultimoImportado.txt','w')
    arquivo.write(ultimaURL)
    arquivo.close     