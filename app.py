## Criar um aplicativo de linha de comando em Python que :

## 1. carrega um dataset do kaggle(CSV)

import kagglehub
import os
import csv

# Download do dataset e retornar o caminho dos arquivos CSV
caminho_dos_arquivos = kagglehub.dataset_download("carrie1/ecommerce-data")
                                                   

# Analisar os arquivos disponiveis
print("Arquivos disponíveis no dataset:")
for arquivo in os.listdir(caminho_dos_arquivos):
    print(f" - {arquivo}")

# Foi registrado um único arquivo CSV no dataset:data.csv
# Definir o caminho completo do arquivo CSV
caminho_csv = os.path.join(caminho_dos_arquivos, "data.csv")

# Abrir o arquivo CSV e ler as colunas
with open(caminho_csv, mode='r', encoding='utf-8') as arquivo_csv:
    leitor_csv = csv.DictReader(arquivo_csv)
    colunas = leitor_csv.fieldnames
    print("Colunas disponíveis no CSV:")
    for coluna in colunas:
        print(f" - {coluna}")

## Colunas encontradas:
#- InvoiceNo = id único da fatura
#- StockCode = código do produto
#- Description = descrição do produto
#- Quantity = quantidade
#- InvoiceDate = data da fatura
#- UnitPrice = preço unitário
#- CustomerID = id do cliente
#- Country = país

# Analisar os 10 primeiros registros
print("\n10 primeiros registros do CSV:")
print("[ ")
for i, registro in enumerate(leitor_csv):
    if i < 10:
        # formato json para melhor visualização, sendo uma coluna por linha
        print(f"   {i+1}",":{ ")
        for chave, valor in registro.items():
            print(f"    {chave}: {valor}")
        print("    },")  # linha em branco entre registros
    else:
        break
print("]")

# lista_exemplo =
# [
#    1 :{
#     InvoiceNo: 536365
#     StockCode: 85123A
#     Description: WHITE HANGING HEART T-LIGHT HOLDER
#     Quantity: 6
#     InvoiceDate: 12/1/2010 8:26
#     UnitPrice: 2.55
#     CustomerID: 17850
#     Country: United Kingdom
#     },
#    2 :{
#     InvoiceNo: 536365
#     StockCode: 71053
#     Description: WHITE METAL LANTERN
#     Quantity: 6
#     InvoiceDate: 12/1/2010 8:26
#     UnitPrice: 3.39
#     CustomerID: 17850
#     Country: United Kingdom
#     },
#    3 :{
#     InvoiceNo: 536365
#     StockCode: 84406B
#     Description: CREAM CUPID HEARTS COAT HANGER
#     Quantity: 8
#     InvoiceDate: 12/1/2010 8:26
#     UnitPrice: 2.75
#     CustomerID: 17850
#     Country: United Kingdom
#     },
#    4 :{
#     InvoiceNo: 536365
#     StockCode: 84029G
#     Description: KNITTED UNION FLAG HOT WATER BOTTLE
#     Quantity: 6
#     InvoiceDate: 12/1/2010 8:26
#     UnitPrice: 3.39
#     CustomerID: 17850
#     Country: United Kingdom
#     },
#    5 :{
#     InvoiceNo: 536365
#     StockCode: 84029E
#     Description: RED WOOLLY HOTTIE WHITE HEART.
#     Quantity: 6
#     InvoiceDate: 12/1/2010 8:26
#     UnitPrice: 3.39
#     CustomerID: 17850
#     Country: United Kingdom
#     },
#    6 :{
#     InvoiceNo: 536365
#     StockCode: 22752
#     Description: SET 7 BABUSHKA NESTING BOXES
#     Quantity: 2
#     InvoiceDate: 12/1/2010 8:26
#     UnitPrice: 7.65
#     CustomerID: 17850
#     Country: United Kingdom
#     },
#    7 :{
#     InvoiceNo: 536365
#     StockCode: 21730
#     Description: GLASS STAR FROSTED T-LIGHT HOLDER
#     Quantity: 6
#     InvoiceDate: 12/1/2010 8:26
#     UnitPrice: 4.25
#     CustomerID: 17850
#     Country: United Kingdom
#     },
#    8 :{
#     InvoiceNo: 536366
#     StockCode: 22633
#     Description: HAND WARMER UNION JACK
#     Quantity: 6
#     InvoiceDate: 12/1/2010 8:28
#     UnitPrice: 1.85
#     CustomerID: 17850
#     Country: United Kingdom
#     },
#    9 :{
#     InvoiceNo: 536366
#     StockCode: 22632
#     Description: HAND WARMER RED POLKA DOT
#     Quantity: 6
#     InvoiceDate: 12/1/2010 8:28
#     UnitPrice: 1.85
#     CustomerID: 17850
#     Country: United Kingdom
#     },
#    10 :{
#     InvoiceNo: 536367
#     StockCode: 84879
#     Description: ASSORTED COLOUR BIRD ORNAMENT
#     Quantity: 32
#     InvoiceDate: 12/1/2010 8:34
#     UnitPrice: 1.69
#     CustomerID: 13047
#     Country: United Kingdom
#     },
# ]


