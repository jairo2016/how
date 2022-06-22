Arquivos de código responsáveis pela ingestão de dados da Pesquisa Mensal de Comércio(PMC) no Big Data de Varejo salvando no AWS S3:
(esses arquivos .xls contêm os índices de crescimento de vendas do comércio varejista por categoria de produto e são disponibilizados mensalmente)
pmcRAW.py: responsável pela camada raw de carga dos arquivos .xls (dados brutos) no bucket arquivosPMCs3 da AWS.
