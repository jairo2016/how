import requests
import datetime
import eventlet
import urllib

url = 'https://ftp.ibge.gov.br/Comercio_e_Servicos/Pesquisa_Mensal_de_Comercio/Tabelas/2018/pmc_201801_04.xls'



with eventlet.Timeout(None):
    urllib.request.urlretrieve(url, 'arquivosPMC/' + url[85:102])

exit()

print('***** verifica url - ' + str(datetime.datetime.now()))
print(url)
response = requests.get(url, verify=False, timeout=None)

if response.status_code == 200:
    #print('Web site exists')
    print('..... baixa arquivo - ' + str(datetime.datetime.now()))
    with eventlet.Timeout(None):
        urllib.request.urlretrieve(url, 'arquivosPMC/' + url[85:102])

    print('..... arquivo baixado - ' + str(datetime.datetime.now()))