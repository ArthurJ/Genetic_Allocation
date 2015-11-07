import numpy as np
import sys
from random import random
from random import choice
from datetime import datetime
from collections import OrderedDict as dict

'''
Created on 10/11/2012
'''
__author__ = '@arthurj'


def should_raise(e):
    if e.args[0] in ('CRASH',):
        pass
    else:
        raise e


def temporizador(func):
    def wrap(*args):
        t = datetime.now()
        res = func(*args)
        tempo = datetime.now() - t
        print('Tempo de Processamento:', tempo)
        return res

    return wrap


def shuffle(genes_originais, prob=0.035):
    genes = list(genes_originais)
    for i, j in enumerate(genes):
        if prob > random():
            k = genes.index(choice(genes))
            genes[i], genes[k] = genes[k], genes[i]
    return tuple(genes)


def ler(nome_arq):
    """
        Lê o arquivo, cria a tabela e as relações entre horarios-linhas
    e entre professores-colunas.
        Retorna a tabela pura e os 2 dicionarios de relacionamento.

    :param nome_arq: Nome do arquivo
    """

    tabela = list()

    with open(nome_arq, 'r') as conteudo:
        tabela = [[celula.replace(' ', '').replace('\n', '').replace('\t', '')
                   for celula in linha.split(';')]
                  for linha in conteudo.readlines()
                  if linha.startswith('#') is not True]

    horarios_t = [[horario[0].split('!')[0], indice - 1]
                  for indice, horario in enumerate(tabela)
                  if horario[0] is not '' and not horario[0].startswith('!')]

    horarios = dict()
    for i, hora_t in enumerate(horarios_t):
        if i + 1 != len(horarios_t):
            final = horarios_t[i + 1][1]
        else:
            final = len(tabela) - 1
        horarios[hora_t[0]] = tuple(list(range(hora_t[1], final)))

    professores_t = [[nome, indice - 1]
                     for indice, nome in enumerate(tabela[0])
                     if nome is not '']

    professores = dict()
    for i, nome_t in enumerate(professores_t):
        if i + 1 != len(professores_t):
            final = professores_t[i + 1][1]
        else:
            final = len(tabela) - 1
        professores[nome_t[0]] = tuple(list(range(nome_t[1], final)))

    tabela = np.array([[float(v) for v in valor[1:] if v != ''] for valor in tabela[1:]])
    return tabela, horarios, professores


def relatorio(somo, entrada, f=sys.stdout):
    print('Satisfação média desta Organização:', '{0:.2f}%'.format(somo.nota * 10), file=f)
    print(somo.genes, file=f)
    if somo.contador_zeros > 0:
        print('Quantidade de notas zero:', somo.contador_zeros, file=f)
    horarioinv = {entrada[1][chave]: chave for chave in entrada[1]}
    professoresinv = {entrada[2][chave]: chave for chave in entrada[2]}
    for colunas in professoresinv:
        print('\n', professoresinv[colunas], '(' + str(+len(colunas)) + ' aulas)' + ',', file=f)
        media = 0
        for coluna in colunas:
            linha = somo.genes.index(coluna)
            for linhas in horarioinv:
                if linha in linhas:
                    media += entrada[0][linha][coluna]
                    print('', horarioinv[linhas] + ' (Linha:' + str(linha) + ');',
                          ' Satisfação:  ' + str(entrada[0][linha][coluna] * 10) + '%', sep='\t', file=f)
        media /= len(colunas)
        print('\n', '\t' * 6 + '[Satisfação média:\t{0:.1f}%]\n'.format(media * 10), end='', file=f)
        print('.' * 60, file=f)
    print('\n', file=f)
