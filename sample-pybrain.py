from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
import os

os.system('cls' if os.name == 'nt' else 'clear') # limpa o terminal
loadbar = ['          ','=         ','==        ','===       ','====      ','=====     ','======    ','=======   ','========  ','========= ']
cont = 0
dataset = SupervisedDataSet(2,1)      # cria e popula o dataset com 2 entradas e uma saida
dataset.addSample((0.8, 0.4), (0.70)) # .addSample() aceita tuplas para popular o dataset
dataset.addSample((0.5, 0.7), (0.50))
dataset.addSample((1.0, 0.8), (0.95))

neuralNetwork = buildNetwork(2, 4, 1, bias = True) # cria a rede neural com 2 neuronios de entrada, 4 ocultos e 1 de saida
trainer = BackpropTrainer(neuralNetwork, dataset)  # cria treinador

for i in range(2000): # treina rede neural
    erro = trainer.train()
    if i%20 == 0: 
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Treinando Rede neural: [' + loadbar[int(cont/10)] + ']  ' + str((cont)) + '%')
        cont+=1

os.system('cls' if os.name == 'nt' else 'clear')
print('Treinando Rede neural: [==========] 100%\n'
     +'Treinamento completo!')
print('O erro encontrado é de ' + str(round(erro*100,2)) + '%.')

while(True):
    d = float(input('Dormiu: '))
    e = float(input('Estudou: '))
    res = neuralNetwork.activate((d/10,e/10)) # ativa rede neural
    print('\nA nota prevista é: ' + str(round(res[0]*10,1)) + '.\n')
    op = input('Continuar?\n')
    if op != 'Sim' and op != 'sim' and op != 'SIM':
        break

print('\nRede neural finalizada!')