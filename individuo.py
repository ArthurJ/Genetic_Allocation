from tools import shuffle

__author__ = '@arthurj'


class Individuo:
    """
    Desenvolvido com a ajuda (na modelagem) do professor
        Francisco Javier Ropero Pelaez
    Somo:
        (Cromossomo) representa um indivíduo formado por genes e uma nota,
            que deve ser dada de acordo com o desempenho obtido no ambiente.
    """

    def __init__(self, tabela, horarios, professores, genes=None):
        if genes is None:
            genes = list(range(len(tabela)))
            genes = tuple(shuffle(genes, prob=.8))
        self.genes = genes
        self.nota = 0
        if self.crash_case(horarios, professores):
            raise Exception('CRASH')
        self.contador_zeros = 0
        self.idade = 0
        self.avaliar(tabela)  # avaliação plana

    def avaliar(self, tabela):
        nota = 0
        qtd_individuos = len(tabela)
        for i, j in enumerate(self.genes):
            if tabela[i][j] == 0:
                self.contador_zeros += 1
                nota -= qtd_individuos * 5
            else:
                nota += tabela[i][j]
        self.nota += nota / len(tabela)

    def crash_case(self, horarios, professores):
        for hora in horarios:
            for nome in professores:
                count = 0
                for i in professores[nome]:
                    for j in horarios[hora]:
                        if i is self.genes[j]:
                            count += 1
                if count >= 2:
                    return True
        return False

    def __lt__(self, other):
        if self.nota == other.nota and \
                        self.contador_zeros > other.contador_zeros:
            return True
        if self.nota < other.nota:
            return True
        else:
            return False

    def __le__(self, other):
        if self.nota == other.nota and \
                        self.contador_zeros > other.contador_zeros:
            return True
        if self.nota <= other.nota:
            return True
        else:
            return False

    def __gt__(self, other):
        if self.nota == other.nota and \
                        self.contador_zeros < other.contador_zeros:
            return True
        if self.nota > other.nota:
            return True
        else:
            return False

    def __ge__(self, other):
        if self.nota == other.nota and \
                        self.contador_zeros < other.contador_zeros:
            return True
        if self.nota >= other.nota:
            return True
        else:
            return False

    def __eq__(self, other):
        if self.nota == other.nota and \
                        self.genes == other.genes:
            return True
        else:
            return False

    def __str__(self):
        zeros = ''
        inconsistencia = ''
        if self.contador_zeros > 0:
            zeros = '     (' + str(self.contador_zeros) + ' zeros)'
        return inconsistencia + str(self.genes) + ' Nota:{0:.2f} '.format(self.nota) + zeros

    def __hash__(self):
        return hash(self.genes)
