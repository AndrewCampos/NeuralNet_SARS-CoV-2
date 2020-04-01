# Neural Network SARS-CoV-2

Rede Neural utilizada para prever estado de casos suspeitos de Covid-19 com base em dados de exames do Hospital Israelita Albert Einstein.

## O problema do SARS-CoV-2

A Organização Mundial da Saúde (OMS) caracterizou a  doença COVID-19, causada pelo virus SARS-CoV-2, como pandêmica no dia 11 de Março de 2020. O crescimento exponencial dos números de infectados foram uma grande preocupação graças ao fato de que a enorme quantidade de pessoas precisando de cuidados médicos e aparelhos específicos causou uma sobrecarga dos sistemas de saúde por todo mundo.

No Brasil o primeiro caso foi registrado no dia 26 de Fevereiro e até o dia 27 de Março, apenas no estado de São Paulo, os hospitais registraram 1.223 casos confirmados com 68 mortes. Dentre eles Hospital Israelita Albert Einstein registrou 477 casos cnonfirmados associados à 30 mortes.

Brazil recorded the first case of SARS-CoV-2 on February 26, and the virus transmission evolved from imported cases only, to local and finally community transmission very rapidly, with the federal government declaring nationwide community transmission on March 20.

O grande problema da COVID-19 é o rápido contágio e agravamento do quadro clínico, fazendo com que seja difícil agir com rapidez. Atualmente devido ao inicio do sobrecarregamento do sistema de saúde, diagnosticar casos suspeitos se tornou um desafio, uma vez que não existem teste suficientes disponíveis para aplicar a todos suspeitos tornando impossível diagnosticar todos os casos.

## Conjunto de Dados

O conjunto de dados contém o relatório médico anônimo de todos os pacientes submetidos ao teste para o SARS-CoV-2 que passaram pelo Hospital Israelita Albert Einstein. Além do resultado do teste para o vírus o relatório também contém outros dados sobre testes laboratoriais em que o paciente foi submetido, além de informar se o mesmo necessitou de internação e qual ala foi enviado (Ala Geral, Tratamento Semi-Intensivo ou Tratamento Intensivo).

## Objetivos

### Objetivo 1

• Baseado nos relatórios laboratoriais, é necessário predizer se o paciente contém ou não o vírus SARS-CoV-2.

### Objetivo 2

• Predizer à partir dos casos de possível presença do vírus se o paciente necessitará de tratamento especializado e em qual ala precisará ser internado se for o caso.

## Tratamento dos Dados

Nos relatórios disponibilizados pelo hospital existem tanto dados numéricos, como rótulos escritos e dados nulos, porém para que a rede neural possa trata-los todos os dados devem estar na forma numérica. Para isso foi adotada a seguinte convenção:

• Dados nulos foram adotados como o valor -1,  
• Rótulos 'positive' foram adotados como 1,  
• Rótulos 'negative' foram adotados como 0,  
• Rótulos 'detectet' foram adotados como 1,
• Rótulos 'not_detected' foram adotados como 0 e
• Rótulos 'not_done' foram adotados como -1.

As os dados presentes nas counas à partir de "Rods #" foram descartados, uma vez que não tinham densidade suficiente para treinar nem testar a rede.

## A Rede Neural

A rede foi criada com o auxílio da biblioteca *PyBrain*, que cria uma rede neural com o aprendizado baseado em reforço, ou seja, o treinamento se dá por diversas iterações seguidas onde os pesos são redefinidos a cada passagem baseados na comparação do resultado previsto com o resultado real. A documentação da biblioteca pode ser encontrada proprio site da  [PyBrain](http://pybrain.org/docs/).

## Resultados

A rede até o momento é eficiente porém não completa. Para um conjunto de 123 individuos de teste, 5522 individuos para treinamento e 100 ciclos de treinamento a rede teve uma taxa de acerto de aproximadamente 81,3%, sendo que acertou cerca de 87% dos diagnosticos sobre a presença do SARS-CoV-2. Seu único problema é que ainda não é eficaz para a predição do tipo de tratamento que cada paciente. Ainda não foi avaliado se essa deficiência na rede é causada pela falta de dados para treinamento ou pela proria arquitetura do programa.

## Referências

O desafio foi proposto pelo próprio Hospital Israelita Albert Einstein, que também forneceu todos os dados, tanto para o mesmo ser realizado quanto os presentes neste texto. por meio do site [Kaggle](https://www.kaggle.com/dataset/e626783d4672f182e7870b1bbe75fae66bdfb232289da0a61f08c2ceb01cab01?fbclid=IwAR3TwoAO658qv48xfTphad9v42FAWUGpb3-KM72D4myV0sS8_tzLgWnb78E).
