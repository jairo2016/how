''' MontaCatComercioParquet:
    recebe a tabela de percentual de crescimento de vendas de comércio por categoria de produto
    e grava em arquivo parquet
'''

import pandas as pd

def Monta_CatComercio_parquet(tabela, ano, mes, PathArquivoParquet):
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

        m1anterior.append(str(tabela.row(linhaXLS)[1].value).replace('- ','0'))
        m2anterior.append(str(tabela.row(linhaXLS)[2].value).replace('- ','0'))
        m3anterior.append(str(tabela.row(linhaXLS)[3].value).replace('- ','0'))
        m1anteriorD.append(str(tabela.row(5)[1].value) + ' - Mês anterior')
        m2anteriorD.append(str(tabela.row(5)[2].value) + ' - Mês anterior')
        m3anteriorD.append(str(tabela.row(5)[3].value) + ' - Mês anterior')

        m1mensal.append(str(tabela.row(linhaXLS)[4].value).replace('- ','0'))
        m2mensal.append(str(tabela.row(linhaXLS)[5].value).replace('- ','0'))
        m3mensal.append(str(tabela.row(linhaXLS)[6].value).replace('- ','0'))
        m1mensalD.append(str(tabela.row(5)[4].value) + ' - Mensal')
        m2mensalD.append(str(tabela.row(5)[5].value) + ' - Mensal')
        m3mensalD.append(str(tabela.row(5)[6].value) + ' - Mensal')

        m1acumulado.append(str(tabela.row(linhaXLS)[7].value).replace('- ','0'))
        m2acumulado.append(str(tabela.row(linhaXLS)[8].value).replace('- ','0'))
        m3acumulado.append(str(tabela.row(linhaXLS)[9].value).replace('- ','0'))
        m1acumuladoD.append(str(tabela.row(5)[7].value) + ' - Acumulado no ano')
        m2acumuladoD.append(str(tabela.row(5)[8].value) + ' - Acumulado no ano')
        m3acumuladoD.append(str(tabela.row(5)[9].value) + ' - Acumulado no ano')

        m1u12m.append(str(tabela.row(linhaXLS)[10].value).replace('- ','0'))
        m2u12m.append(str(tabela.row(linhaXLS)[11].value).replace('- ','0'))
        m3u12m.append(str(tabela.row(linhaXLS)[12].value).replace('- ','0'))
        m1u12mD.append(str(tabela.row(5)[10].value) + ' - Últimos 12 meses')
        m2u12mD.append(str(tabela.row(5)[11].value) + ' - Últimos 12 meses')
        m3u12mD.append(str(tabela.row(5)[12].value) + ' - Últimos 12 meses')

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
    else:
        return False