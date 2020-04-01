import csv 

primeiro = True
dados  = []
FILE   = 'einsteinDataset.csv'
try:
    arquivo = open(FILE) # abre o arquivo
except:
    print('\nErro ao abrir o arquivo "'+ FILE +'".\n'+'\033[31m'+'ABORTADO!'+'\033[0;0m')
    exit(-1)
else:
    print('Arquivo "'+FILE+'" carregado com'+'\033[32m'+' sucesso!'+'\033[0;0m')
linhas = csv.reader(arquivo) # bufferiza o arquivo e salva em linhas
for linha in linhas: # transforma o arquivo csv bufferizado em tuplas
    for i in range(len(linha)): # trata as execões do .csv
        if linha[i] == '':
            linha[i] = '-1'
        elif linha[i] == 'not_detected':
            linha[i] = '0'
        elif linha[i] == 'detected':
            linha[i] = '1'
        elif linha[i] == 'positive':
            linha[i] = '1'
        elif linha[i] == 'negative':
            linha[i] = '0'
        elif linha[i] == 'not_done':
            linha[i] = '-1'
        try:
            linha[i] = str(float(linha[i])/100)
        except:  continue
    if primeiro:
        primeiro = False
        dados.append(linha[:65]) # apenas pra teste
    else:
        try:
            j = float(linha[1])
        except:
            continue
        else:
            dados.append(linha[:65])

print('\nNumero de Colunas:',f'{len(dados[0]):>5}')
print('Numero de Linhas: ',f'{len(dados):>5}')

teste = ''

for i in dados[1]:
    if i == '':
        print('ué')
    else:
        print(i)
