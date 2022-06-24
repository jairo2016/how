''' CAMADA SILVER:
    LE OS ARQUIVOS .xls BAIXADOS DO IBGE, COM ETL SEPARA AS TABELAS AGRUPADAS POR UF DAS
    TABELAS AGRUPADAS POR CLASSES DE COMÉRCIO, SELECIONA AS COLUNAS NECESSÁRIAS
    TRANSFORMANDO EM ARQUIVOS PARQUET, ARMAZENANDO NO BUCKET arquivosPMCprocessedS3 E 
    DISPONIBILIZANDO PARA A CAMADA GOLD
'''

from ast import Try
import os
from socket import timeout
import urllib.request
from numpy import setxor1d
import requests
import datetime
import eventlet

import uploadS3 as upds3
import pandas as pd
import xlrd
import strip



def Monta_CLASSE_COMERCIO_parquet(tabela, ano, mes, PathArquivoParquet):
    qtd_linhas = tabela.nrows
    linhaXLS= 6
    i=0
    
    registro= []
    descricao= []

    m1anterior= []
    m2anterior= []
    m3anterior= []

    m1anteriorD= []
    m2anteriorD= []
    m3anteriorD= []

    m1mensal= []
    m2mensal= []
    m3mensal= []

    m1mensalD= []
    m2mensalD= []
    m3mensalD= []    

    m1acumulado= []
    m2acumulado= []
    m3acumulado= []

    m1acumuladoD= []
    m2acumuladoD= []
    m3acumuladoD= []

    m1u12m= []
    m2u12m= []
    m3u12m= []   

    m1u12mD= []
    m2u12mD= []
    m3u12mD= []    

    m1anomes= []
    m2anomes= []
    m3anomes= []               

    while linhaXLS <= qtd_linhas:
        valor= tabela.row(linhaXLS)[1].value
        if str(valor) == '-':
            valor = 0

        try:
            float(valor)
        except ValueError:
            break

        try:
            testa= tabela.row(6)[7].value
        except IndexError:
            break

        i= i+1
        registro.append(i)
        descricao.append(tabela.row(linhaXLS)[0].value)

        m1anterior.append(str(tabela.row(linhaXLS)[1].value).replace('-','0'))
        m2anterior.append(str(tabela.row(linhaXLS)[2].value).replace('-','0'))
        m3anterior.append(str(tabela.row(linhaXLS)[3].value).replace('-','0'))
        m1anteriorD.append(str(tabela.row(6)[1].value) + ' - Mês anterior')
        m2anteriorD.append(str(tabela.row(6)[2].value) + ' - Mês anterior')
        m3anteriorD.append(str(tabela.row(6)[3].value) + ' - Mês anterior')

        m1mensal.append(str(tabela.row(linhaXLS)[4].value).replace('-','0'))
        m2mensal.append(str(tabela.row(linhaXLS)[5].value).replace('-','0'))
        m3mensal.append(str(tabela.row(linhaXLS)[6].value).replace('-','0'))
        m1mensalD.append(str(tabela.row(6)[4].value) + ' - Mensal')
        m2mensalD.append(str(tabela.row(6)[5].value) + ' - Mensal')
        m3mensalD.append(str(tabela.row(6)[6].value) + ' - Mensal')

        m1acumulado.append(str(tabela.row(linhaXLS)[7].value).replace('-','0'))
        m2acumulado.append(str(tabela.row(linhaXLS)[8].value).replace('-','0'))
        m3acumulado.append(str(tabela.row(linhaXLS)[9].value).replace('-','0'))
        m1acumuladoD.append(str(tabela.row(6)[7].value) + ' - Acumulado no ano')
        m2acumuladoD.append(str(tabela.row(6)[8].value) + ' - Acumulado no ano')
        m3acumuladoD.append(str(tabela.row(6)[9].value) + ' - Acumulado no ano')

        m1u12m.append(str(tabela.row(linhaXLS)[10].value).replace('-','0'))
        m2u12m.append(str(tabela.row(linhaXLS)[11].value).replace('-','0'))
        m3u12m.append(str(tabela.row(linhaXLS)[12].value).replace('-','0'))
        m1u12mD.append(str(tabela.row(6)[10].value) + ' - Últimos 12 meses')
        m2u12mD.append(str(tabela.row(6)[11].value) + ' - Últimos 12 meses')
        m3u12mD.append(str(tabela.row(6)[12].value) + ' - Últimos 12 meses')

        mes_2= int(mes) -2
        mes_1= int(mes) -1
        mes_2 = '%02d' % mes_2
        mes_1 = '%02d' % mes_1
        m1anomes.append(str(ano) + str(mes_2))
        m2anomes.append(str(ano) + str(mes_1))
        m3anomes.append(str(ano) + str(mes))          

        linhaXLS=linhaXLS+1

    if i>0:
        df=pd.DataFrame({
                "registro":registro,
                "classe_comercio":descricao,

                "m1anterior":m1anterior,
                "m2anterior":m2anterior,
                "m3anterior":m3anterior,
                "m1anteriorD":m1anteriorD,
                "m2anteriorD":m2anteriorD,
                "m3anteriorD":m3anteriorD,

                "m1mensal":m1mensal,
                "m2mensal":m2mensal,
                "m3mensal":m3mensal,
                "m1mensalD":m1mensalD,
                "m2mensalD":m2mensalD,
                "m3mensalD":m3mensalD,

                "m1acumulado":m1acumulado,
                "m2acumulado":m2acumulado,
                "m3acumulado":m3acumulado,
                "m1acumuladoD":m1acumuladoD,
                "m2acumuladoD":m2acumuladoD,
                "m3acumuladoD":m3acumuladoD,

                "m1u12m":m1u12m,
                "m2u12m":m2u12m, 
                "m3u12m":m3u12m,
                "m1u12mD":m1u12mD,
                "m2u12mD":m2u12mD, 
                "m3u12mD":m3u12mD,

                "m1anomes":m1anomes,
                "m2anomes":m2anomes,
                "m3anomes":m3anomes,
                })

        df.to_parquet(PathArquivoParquet + '.pq')
        df.to_string(PathArquivoParquet + '.txt')
        return True

def Monta_UF_parquet(tabela, ano, mes, PathArquivoParquet):
    qtd_linhas = tabela.nrows
    linhaXLS= 6
    i=0
    
    registro= []
    descricao= []

    m1anterior= []
    m2anterior= []
    m3anterior= []

    m1anteriorD= []
    m2anteriorD= []
    m3anteriorD= []

    m1mensal= []
    m2mensal= []
    m3mensal= []

    m1mensalD= []
    m2mensalD= []
    m3mensalD= []    

    m1acumulado= []
    m2acumulado= []
    m3acumulado= []

    m1acumuladoD= []
    m2acumuladoD= []
    m3acumuladoD= []

    m1u12m= []
    m2u12m= []
    m3u12m= []   

    m1u12mD= []
    m2u12mD= []
    m3u12mD= []    

    m1anomes= []
    m2anomes= []
    m3anomes= []               

    while linhaXLS <= qtd_linhas:
        valor= tabela.row(linhaXLS)[1].value
        if str(valor) == '-':
            valor = 0

        try:
            float(valor)
        except ValueError:
            break

        try:
            testa= tabela.row(6)[7].value
        except IndexError:
            break

        i= i+1
        registro.append(i)
        descricao.append(tabela.row(linhaXLS)[0].value)

        m1anterior.append(str(tabela.row(linhaXLS)[1].value).replace('-','0'))
        m2anterior.append(str(tabela.row(linhaXLS)[2].value).replace('-','0'))
        m3anterior.append(str(tabela.row(linhaXLS)[3].value).replace('-','0'))
        m1anteriorD.append(str(tabela.row(6)[1].value) + ' - Mês anterior')
        m2anteriorD.append(str(tabela.row(6)[2].value) + ' - Mês anterior')
        m3anteriorD.append(str(tabela.row(6)[3].value) + ' - Mês anterior')

        m1mensal.append(str(tabela.row(linhaXLS)[4].value).replace('-','0'))
        m2mensal.append(str(tabela.row(linhaXLS)[5].value).replace('-','0'))
        m3mensal.append(str(tabela.row(linhaXLS)[6].value).replace('-','0'))
        m1mensalD.append(str(tabela.row(6)[4].value) + ' - Mensal')
        m2mensalD.append(str(tabela.row(6)[5].value) + ' - Mensal')
        m3mensalD.append(str(tabela.row(6)[6].value) + ' - Mensal')

        m1acumulado.append(str(tabela.row(linhaXLS)[7].value).replace('-','0'))
        m2acumulado.append(str(tabela.row(linhaXLS)[8].value).replace('-','0'))
        m3acumulado.append(str(tabela.row(linhaXLS)[9].value).replace('-','0'))
        m1acumuladoD.append(str(tabela.row(6)[7].value) + ' - Acumulado no ano')
        m2acumuladoD.append(str(tabela.row(6)[8].value) + ' - Acumulado no ano')
        m3acumuladoD.append(str(tabela.row(6)[9].value) + ' - Acumulado no ano')

        m1u12m.append(str(tabela.row(linhaXLS)[10].value).replace('-','0'))
        m2u12m.append(str(tabela.row(linhaXLS)[11].value).replace('-','0'))
        m3u12m.append(str(tabela.row(linhaXLS)[12].value).replace('-','0'))
        m1u12mD.append(str(tabela.row(6)[10].value) + ' - Últimos 12 meses')
        m2u12mD.append(str(tabela.row(6)[11].value) + ' - Últimos 12 meses')
        m3u12mD.append(str(tabela.row(6)[12].value) + ' - Últimos 12 meses')

        mes_2= int(mes) -2
        mes_1= int(mes) -1
        mes_2 = '%02d' % mes_2
        mes_1 = '%02d' % mes_1
        m1anomes.append(str(ano) + str(mes_2))
        m2anomes.append(str(ano) + str(mes_1))
        m3anomes.append(str(ano) + str(mes))          

        linhaXLS=linhaXLS+1

    if i>0:
        df=pd.DataFrame({
                "registro":registro,
                "UF":descricao,

                "m1anterior":m1anterior,
                "m2anterior":m2anterior,
                "m3anterior":m3anterior,
                "m1anteriorD":m1anteriorD,
                "m2anteriorD":m2anteriorD,
                "m3anteriorD":m3anteriorD,

                "m1mensal":m1mensal,
                "m2mensal":m2mensal,
                "m3mensal":m3mensal,
                "m1mensalD":m1mensalD,
                "m2mensalD":m2mensalD,
                "m3mensalD":m3mensalD,

                "m1acumulado":m1acumulado,
                "m2acumulado":m2acumulado,
                "m3acumulado":m3acumulado,
                "m1acumuladoD":m1acumuladoD,
                "m2acumuladoD":m2acumuladoD,
                "m3acumuladoD":m3acumuladoD,

                "m1u12m":m1u12m,
                "m2u12m":m2u12m, 
                "m3u12m":m3u12m,
                "m1u12mD":m1u12mD,
                "m2u12mD":m2u12mD, 
                "m3u12mD":m3u12mD,

                "m1anomes":m1anomes,
                "m2anomes":m2anomes,
                "m3anomes":m3anomes,
                })

        df.to_parquet(PathArquivoParquet + '.pq')
        df.to_string(PathArquivoParquet + '.txt')
        return True

def le_xls(arquivo):
    tabela = xlrd.open_workbook(arquivo).sheet_by_index(0)
    return tabela    



# verifica se a pasta arquivosPMCprocessed existe e, se não, cria a mesma
if os.path.exists('arquivosPMCprocessed') == False:
    os.mkdir('arquivosPMCprocessed')

# verifica se a pasta ultimoProcessado existe e, se não, cria a mesma
if os.path.exists('ultimoProcessado') == False:
    os.mkdir('ultimoProcessado')    

# verifica se o arquivo ultimoProcessado.txt existe e, se não, cria o mesmo
if os.path.exists('ultimoProcessado/ultimoProcessado.txt') == False:
    arquivo = open('ultimoProcessado/ultimoProcessado.txt','w')
    arquivo.write("vazio")
    arquivo.close

# lê o arquivo ultimoProcessado.txt para pegar o último arquivo .xls transformado em parquet
linha='vazio'
arquivo = open('ultimoProcessado/ultimoProcessado.txt','r')
for linha in arquivo:
    linha = linha.rstrip()
arquivo.close()

# verifica se o arquivo ultimoProcessado.txt tem a informação do último arquivo.xls transformado em parquet
if linha == 'vazio':
    url = 'pmc_201800_00.xls'   
else:
    url = linha

ultimoArquivoProcessado = ''
seq = url[11:13]
seq = int(seq) + 1
seq = '%02d' % seq

ano= url[4:8]
anomes= url[4:10]
mes= anomes[5:7]

anomes = int(anomes) + 1
mes= int(mes) + 1
mes = '%02d' % mes

nomeArq= 'pmc_{}_{}.xls'
anocorrente = datetime.date.today().year

while int(ano) <= int(anocorrente):

    while int(mes) <= 12:

        while int(seq) <= 13:

            #print(nomeArq.format(anomes, seq))

            # verifica se o arquivo arquivoPMCprocessed .xls existe e processa o mesmo
            arquivo= 'arquivosPMCraw/' + nomeArq.format(anomes, seq)

            if os.path.exists(arquivo) == True:
                tabela= le_xls(arquivo)

                if tabela.row(6)[0].value[:6] == 'Brasil':
                    PathArquivoParquet= ('arquivosPMCprocessed/PercUF_' + 
                                         nomeArq.format(anomes, seq)[:13])
                    retorno= Monta_UF_parquet(tabela, ano, mes, PathArquivoParquet)
                else:
                    PathArquivoParquet= ('arquivosPMCprocessed/PercCLASSE_COMERCIO_' + 
                                         nomeArq.format(anomes, seq)[:13])                    
                    retorno= Monta_CLASSE_COMERCIO_parquet(tabela, ano, mes, PathArquivoParquet)

                if retorno == True:
                    ultimoArquivoProcessado = nomeArq.format(anomes, seq)

                #print(nomeArq.format(anomes, seq))

            seq = int(seq) + 1
            seq = '%02d' % seq

        seq= '01'
        mes= int(mes) + 1
        mes = '%02d' % mes
        anomes = int(anomes) + 1

    mes= '01'
    ano= int(ano) + 1
    anomes= str(ano) + str(mes)
    

if len(ultimoArquivoProcessado) > 0: # grava a posição do último arquivo pmc.xls baixado
    arquivo = open('ultimoProcessado/ultimoProcessado.txt','w')
    arquivo.write(ultimoArquivoProcessado)
    arquivo.close 