from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
import csv 
import random

# Variaveis Globais
dados  = [] # dados dos pacientes
FILE   = 'einsteinDataset.csv'
TREINO = 1 # numeros de ciclos de treinamento
qi     = 500 #quantidade de individos teste
iTeste = [] # individuos teste
erro   = 1 # erro do treinador
AG     = 0 # ala geral
SI     = 0 # semi-intensivo
TI     = 0 # intensivo
prec   = 0 # precisao de previsao
alocados  = 0 # leitos alocados
erroLeito = 0 # leitos mal alocados
nTratados = 0 # pacientes nao tratados
mediaErros = 0 # media da taxa de erro por paciente
acertos    = 0 # diagnosticos de COVID-19 corretos
logPath = 'systemLog.txt'

# Imprime a barra de progresso
def progress(atual,max):
    if atual != 0: porc = int(100*atual/max)
    else: porc = 0
    hash = ''
    for i in range(int(porc/5)): hash += '#'
    print('\033[33m' + f'[{hash:<20}]'+  f'{porc:>4}%' + '\033[0;0m',end='\r')

# Abre o arquivo .csv FILE e salva em dados
def abreCSV():
    global log
    cont = 0
    primeiro = True
    try:
        arquivo = open(FILE) # abre o arquivo
    except:
        log.write('\nErro ao abrir o arquivo "'+ FILE +'".\nABORTADO!\n')
        print('\nErro ao abrir o arquivo "'+ FILE +'".\n'+'\033[31m'+'ABORTADO!'+'\033[0;0m')
        exit(-1)
    else:
        log.write('Arquivo "'+FILE+'" carregado com sucesso!\n')
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
        else:
            try:
                j = float(linha[1])
            except:
                continue
            else:
                dados.append(linha[:65])

# Trata a resposta da rede neural e imprime em forma de relatório
def trataRes(res,ID):
    global prec
    global nTratados
    global erroLeito
    global mediaErros
    global alocados
    global acertos
    match = True
    erros  = 0

    if res[0] <= 0.05: res[0] = 0
    else: res[0] = 1
    if res[1] <= 0.05: res[1] = 0
    else: res[1] = 1
    if res[2] <= 0.05: res[2] = 0
    else: res[2] = 1
    if res[3] <= 0.05: res[3] = 0
    else: res[3] = 1

    print('--------------------------------------------------------------\n'
        + 'Paciente '+str(ID[0])+'\n'
        + '--------------------------------------------------------------\n'
        + '               Teste COVID-19                       Internação\n'
        + '               --------------                  ---------------\n'
        + '    Real:',end='')
    
       
    if ID[2] == '0.01': print('            positivo',end='')
    else: print('            negativo',end='')

    if ID[3] == '0.01': print('			     ala geral',end='')
    elif ID[4] == '0.01': print('                   semi-intensivo',end='')
    elif ID[5] == '0.01': print('                       intensivo',end='')
    else: print('                    não internado',end='')
    if res[0] != float(ID[2]): # teste COVID-19
        match = False
        nTratados +=1
        erros+= 1
    else: acertos+=1
    if res[1] != float(ID[3]): # ala geral
        match = False
        erros+= 1
    if res[2] != float(ID[4]): # semi-intensivo
        match = False
        erros+= 1
    if res[3] != float(ID[5]): # intensivo
        match = False
        erros+= 1    

    print('\nPredição:',end='')
    if res[0] == 1: print('            positivo',end='')
    else: print('            negativo',end='')
    if res[1] == 1: 
        print('			     ala geral')
        alocados +=1
        if ID[3] != '0.01': 
            erroLeito +=1
    elif res[2] == 1: 
        print('                   semi-intensivo')
        alocados +=1
        if ID[4] != '0.01':
            erroLeito +=1
    elif res[3] == 1: 
        print('                       intensivo')
        alocados +=1
        if ID[5] != '0.01': 
            erroLeito +=1
    else: 
        print('                    não internado')
        if ID[3] == '0.01' or ID[4] == '0.01' or ID[5] == '0.01':
            nTratados +=1

    if match:
        print('\033[32m'+'\nMatch!'+'\033[0;0m')
    else:
        print('\033[31m'+'\nMismatch!\n'+'\033[0;0m'
            + 'Precisão: ' + str((100*erros/4)) + '%')
        prec += 1

    mediaErros += erros

# Trata a resposta da rede neural e imprime em forma de relatório
def logRes(res,ID):
    match = True
    erros  = 0

    if res[0] <= 0.05: res[0] = 0
    else: res[0] = 1
    if res[1] <= 0.05: res[1] = 0
    else: res[1] = 1
    if res[2] <= 0.05: res[2] = 0
    else: res[2] = 1
    if res[3] <= 0.05: res[3] = 0
    else: res[3] = 1

    log.write('--------------------------------------------------------------\n'
        + 'Paciente '+str(ID[0])+'\n'
        + '--------------------------------------------------------------\n'
        + '               Teste COVID-19                       Internação\n'
        + '               --------------                  ---------------\n'
        + '    Real:')
    
       
    if ID[2] == '0.01': log.write('            positivo')
    else: log.write('            negativo')

    if ID[3] == '0.01': log.write('			     ala geral')
    elif ID[4] == '0.01': log.write('                   semi-intensivo')
    elif ID[5] == '0.01': log.write('                       intensivo')
    else: log.write('                    não internado')
    if res[0] != float(ID[2]): # teste COVID-19
        match = False
    if res[1] != float(ID[3]): # ala geral
        match = False
    if res[2] != float(ID[4]): # semi-intensivo
        match = False
    if res[3] != float(ID[5]): # intensivo
        match = False

    log.write('\nPredição:')
    if res[0] == 1: log.write('            positivo')
    else: log.write('            negativo')
    if res[1] == 1: 
        log.write('			     ala geral\n')
    elif res[2] == 1: 
        log.write('                   semi-intensivo\n')
    elif res[3] == 1: 
        log.write('                       intensivo\n')
    else: 
        log.write('                    não internado\n')

    if match:
        log.write('\nMatch!\n')
    else:
        log.write('\nMismatch!\n')

# Gera a rede neural, treina e roda a predição
def neuralNet():
    c=0
    j=0
    global erro
    global log
    dataset = SupervisedDataSet(len(dados[0])-5,4) # cria e popula o dataset com dados dos exames como 
                                                   # entrada e o resultado para SARS-CoV-2 como saida
    print("Criando Dataset...")                    # juntamente com os tipos de internacao
    log.write('\nCriando Dataset...\n')
    for paciente in dados:
        c+=1
        ID = paciente[0]
        try:
            temp = paciente.copy()
            saida = tuple(paciente[2:6])
            temp.remove(temp[2]) # remove coluna de resultado
            temp.remove(temp[2]) # remove coluna de ala geral
            temp.remove(temp[2]) # remove coluna de semi-intensivo
            temp.remove(temp[2]) # remove coluna de intensivo
            temp.remove(temp[0]) # remove coluna de ID
            entrada = tuple(temp)
            dataset.addSample(entrada,saida) # popula o dataset
        except: 
            log.write('Erro ao inserir no dataset! [ID: '+ID+']\nABORTADO!\n')
            print('\n\033[31m'+'Erro ao inserir no dataset! [ID: '+ID+']\nABORTADO!\n'+'\033[0;0m')
            exit(-1)
        progress(c,len(dados)-1) # atualiza a barra de progresso
    
    log.write('.\nDataset populado com sucesso!\n')
    print('\nDataset populado com sucesso!')
    neuralNetwork = buildNetwork(len(dados[0])-5, 32, 4, bias = True) # cria a rede neural com 2 neuronios de entrada, 4 ocultos e 1 de saida
    trainer = BackpropTrainer(neuralNetwork, dataset)  # cria treinador

    log.write('Treinando rede neural...\n.\n')
    print('Treinando rede neural...')
    progress(0,1) # atualiza a barra de progresso
    for i in range(0,TREINO): 
        erro = trainer.train() # treina rede neural e encontra o erro relativo
        progress(i,TREINO-1) # atualiza a barra de progresso
    
    log.write('Treinamento completo!\n'+'O erro encontrado é de '+str(round(erro*100,2))+'%.\n')
    print('\nTreinamento completo!\n'+'O erro encontrado é de '+'\033[31m'+str(round(erro*100,2))+'%.'+'\033[0;0m')
    op = input('Rede neural pronta para predição.\n'
             + 'Deseja prosseguir? (s/n) ')
    if op.lower() == 'n':
        log.write('Processo parado pelo usuário.\n')
        print('-----------------------------------------------------------------------------------------------------------------------------')
        print('Impossível gerar relatório final.')
        log.write('--------------------------------------------------------------\n')
        log.write('Impossível gerar relatório final.')
        log.close()
        exit(-1)
    elif op.lower() != 's':
        print('Opção Inválida!\n'+'\033[31m'+'ABORTADO!'+'\033[0;0m')
        return
    log.write('Testando rede neural para individuos-teste\n')
    print('Testando rede neural para individuos-teste')
    for p in iTeste:
        ID = p[0]
        entrada = p.copy()
        entrada.remove(entrada[2]) # remove coluna de resultado
        entrada.remove(entrada[2]) # remove coluna de ala geral
        entrada.remove(entrada[2]) # remove coluna de semi-intensivo
        entrada.remove(entrada[2]) # remove coluna de intensivo
        entrada.remove(entrada[0]) # remove ID
        res = neuralNetwork.activate(tuple(entrada)) # ativa rede neural
        trataRes(res,p)
        logRes(res,p)

############################################ MAIN ############################################################
log = open(logPath, 'w')
log.write('--------------------------------------------------------------\n'
    + 'REDE NEURAL PREDITIVA PARA O SARS-CoV-2\n'
    + '--------------------------------------------------------------\n')
print('-----------------------------------------------------------------------------------------------------------------------------\n'
    + 'REDE NEURAL PREDITIVA PARA O SARS-CoV-2\n'
    + '-----------------------------------------------------------------------------------------------------------------------------\n')
abreCSV()

log.write('Escolhendo individuos para teste...\n')
print('Escolhendo individuos para teste...')
for i in range(qi):
    index = random.randint(1,len(dados)-1)
    iTeste.append(dados[index]) # escolhe IDs aleatorios para serem os individuos de teste
    dados.remove(dados[index])

sair = False
while not sair:
    try: 
        TREINO = int(input('Rede neural pronta para treinamento.\n'
                         + 'Insira o número de ciclos: '))
    except: 
        sair = False
        print('\033[31m'+'Valor inserido não é um número!'+'\033[0;0m')
    else:
        log.write('Número de ciclos fornecido: ' + str(TREINO))
        neuralNet()
        sair = True

EPred = round((100-(100*prec/qi)),2)
ETrain = round((100-(erro*100)),2)
malAlocado = round((100*erroLeito/alocados),2)
mediaErros = round(mediaErros/qi,2)
#except:
#    print('-----------------------------------------------------------------------------------------------------------------------------')
#    print('Impossível gerar relatório final.')
#    log.write('--------------------------------------------------------------\n')
#    log.write('Impossível gerar relatório final.')
#    log.close()
#    exit(-1)
    
print('-----------------------------------------------------------------------------------------------------------------------------')
print('Gerando relatório final...'
    + '\nPacientes avaliados:                 ' + f'{qi:>6}'
    + '\nDiagnosticos corretos:               ' + f'{acertos:>6}'
    + '\nPrecisão das previsões:              ' + f'{EPred:>6}%'
    + '\nPrecisão encontrada pelo treinador:  ' + f'{ETrain:>6}%'
    + '\nLeitos alocados:                     ' + f'{alocados:>6}'
    + '\nLeitos mal alocados:                 ' + f'{erroLeito:>6} (' + str(malAlocado) + ')%'
    + '\nPacientes não tratados:              ' + f'{nTratados:>6}'
    + '\nErro médio por paciente:             ' + f'{mediaErros:>6}%')
print('\033[32m'+'Fim da execução!\n'+'\033[0;0m')

log.write('-------------------------------------------------------------------------\n')
log.write('Gerando relatório final...'
    + '\nPacientes avaliados:                 ' + f'{qi:>6}'
    + '\nDiagnosticos corretos:               ' + f'{acertos:>6}'
    + '\nPrecisão das previsões:              ' + f'{EPred:>6}%'
    + '\nPrecisão encontrada pelo treinador:  ' + f'{ETrain:>6}%'
    + '\nLeitos alocados:                     ' + f'{alocados:>6}'
    + '\nLeitos mal alocados:                 ' + f'{erroLeito:>6} (' + str(malAlocado) + ')%'
    + '\nPacientes não tratados:              ' + f'{nTratados:>6}'
    + '\nErro médio por paciente:             ' + f'{mediaErros:>6}%\n')
log.write('Fim da execução!\n')

log.close()
