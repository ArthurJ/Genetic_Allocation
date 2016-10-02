import numpy as np
from tools import shuffle
from copy import deepcopy as copy
from random import choice
from tools import temporizador
from itertools import combinations
from individuo import Individuo
from multiprocessing import Pool
from multiprocessing import cpu_count
from time import sleep
from random import randint

'''
Created on 10/11/2012
Desenvolvido com a ajuda (na modelagem) do professor
    Francisco Javier Ropero Pelaez
'''
__author__ = '@arthurj'


def combinar(genes1, genes2):
    crosspoint = randint(1, len(genes1) - 1)

    conjunto = set(genes1 + genes2)
    genes_a = list(shuffle(genes1))
    genes_b = list(shuffle(genes2))

    genes_f = [genes_a[:crosspoint], genes_b[:crosspoint]]
    complementos = [genes_b[crosspoint:], genes_a[crosspoint:]]

    for genes in genes_f:
        complemento = complementos.pop(0)
        for gene in complemento:
            if gene not in genes:
                genes.append(gene)
            else:
                genes.append(conjunto.difference(genes + complemento).pop())
    return tuple(genes_f[0]), tuple(genes_f[1])


def sex(tabela, horarios, professores, casais):  # reprodução sexuada
    prole = set()
    contador_de_rejeitados = 0
    for casal in casais:
        combinacao = combinar(casal[0].genes, casal[1].genes)
        try:
            somo_a = Individuo(tabela, horarios, professores, combinacao[0])
            prole.add(somo_a)
        except Exception:
            contador_de_rejeitados += 1
        try:
            somo_b = Individuo(tabela, horarios, professores, combinacao[1])
            prole.add(somo_b)
        except Exception:
            contador_de_rejeitados += 1
    return prole


def assex(somos, tabela, horarios, professores):  # reprodção assexuada
    clones = set()
    for somo in somos:
        try:
            clones.add(Individuo(tabela, horarios,
                                 professores, shuffle(list(somo.genes))))
        except Exception:
            pass
    return clones


class População(object):
    """
    Representa uma geração.
    Contém os indivíduos, avaliações, tabela ambiente.
    Responsável por criar a próxima geração.
    """

    def __init__(self, tabela, horarios, professores, somos,
                 max_somos=85, pool=None):
        """
        :param tabela: Matriz n x n com valores entre 1 e 10. "0" implica em
                    restrição severa e não deve ser usado à toa.

        :param horarios: Dicionário de tamenho n, que liga um horário a
                    uma tupla de linhas da tabela.

        :param professores: Dicionário de tamanho <= n,
                    que liga o nome dos professores às colunas da tabela.

        :param max_somos (default=85): Número inteiro positivo maior que 4,
                    que limita o número de somos preservados a cada geração.

        """
        self.num_processos = 2 * cpu_count()
        if pool is None:
            self.pool = Pool(processes=self.num_processos)
        else:
            self.pool = pool

        if somos is None or len(somos) < self.num_processos:
            msg = 'Erro nos argumentos:\n'
            msg += 'Somos não declarados ou número de somos muito pequeno.\n'
            raise Exception(msg)

        self.tabela = np.array(tabela)
        self.horarios = horarios
        self.professores = professores

        self.limits = dict([('max', max_somos), ('min', int(max_somos * .3)),
                            ('top', int(max_somos * .25))])

        self.selecao(somos)
        self.avaliar()

        if len(self.somos) is 0 or self.somos is None:
            raise Exception('População morta não superou as restrições.')

    def selecao(self, somos):
        somos_ = sorted([copy(somo) for somo in somos if somo.nota > 0], reverse=True)
        if len(somos_) < 4:
            somos_ = sorted([copy(somo) for somo in somos], reverse=True)
        set_somos = set(somos_[:self.limits['min']])
        for i in range(len(somos_)):
            escolhido = choice(somos_)
            somos_.remove(escolhido)
            set_somos.add(escolhido)
            if len(set_somos) >= self.limits['max']:
                break
        self.somos = sorted(list(set_somos), reverse=True)

    def avaliar(self):
        notas = [somo.nota for somo in self.somos]
        statistics = [0, 0, 0, 0]
        statistics[0] = self.somos[0].nota
        statistics[1] = self.somos[-1].nota
        statistics[2] = np.mean(notas)
        statistics[3] = np.std(notas)
        self.statistics = tuple(statistics)

    @temporizador
    def next(self):
        novos_somos = set()
        [novos_somos.add(somo)
         for somo in self.somos[:self.limits['top']]]  # manter os melhores

        combinacoes = list(combinations(self.somos, 2))

        procs = []

        passo = int(len(self.somos) / self.num_processos)
        if passo == 0:
            passo += 1
        slices = [[i, i + passo] for i in range(0, len(self.somos), passo)
                  if i < len(self.somos)]
        slices[-1][-1] = -1
        [procs.append(self.pool.apply_async(assex,
                                            (self.somos[i:j], self.tabela,
                                             self.horarios, self.professores)))
         for i, j in slices]

        passo = int(len(combinacoes) / self.num_processos)
        if passo == 0:
            passo += 1
        slices = [[i, i + passo] for i in range(0, len(combinacoes), passo)
                  if i < len(combinacoes)]
        slices[-1][-1] = -1
        [procs.append(self.pool.apply_async(sex,
                                            (self.tabela, self.horarios,
                                             self.professores,
                                             combinacoes[i:j])))
            for i, j in slices]

        while True:
            if np.all([proc.ready() for proc in procs]):
                [novos_somos.update(proc.get()) for proc in procs]
                break
            sleep(.027)
        print('Indivíduos criados com sucesso: ', len(novos_somos))

        self.somos = list()
        self.selecao(novos_somos)
        self.avaliar()

        return self

    def __str__(self):
        s = 'TAMANHO FINAL DA POPULAÇÃO: {0}.\n'.format(len(self.somos))
        s += 'Melhor:{0:.2f}, pior:{1:.2f}, média:{2:.2f}, desvio padrão:{3:.3f};\n'.format(*self.statistics)
        s += 'Melhor representante nesta geração:\n{0}'.format(self.somos[0])
        return s

    def __repr__(self):
        string = self.__str__() + '\n'
        for item in self.somos:
            string += str(item) + '\n'
        return string