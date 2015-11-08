from população import População
from individuo import Individuo
import tools
import os
from datetime import datetime
from multiprocessing import cpu_count
from multiprocessing import freeze_support

__author__ = '@arthurj'

entrada = tools.ler('caso_realista.csv')
res = None
somos = set()
maxi = 80
count = 0
while len(somos) < 5 * cpu_count() + 1:
    count += 1
    if count > 1000:
        print("[ATENÇÃO!] Atingiu o limite de tentativas de criar somos")
        break
    try:
        s = Individuo(*entrada)
        somos.add(s)
    except Exception as e:
        tools.should_raise(e)

print('Quantidade de somos iniciais:', len(somos), '\n' + '.' * 60)


@tools.temporizador
def iterar(g, max_wait_4_new_fitness=20):
    melhor_passado = list()
    for i in range(1, 1000):
        print('--', str(i) + 'ª', 'Geração --')
        g.next()
        print(g)
        melhor_passado.append(g.somos[0].nota)
        print('[' + str(melhor_passado.count(g.somos[0].nota)) +
              'ª ocorrência desta nota]', '\n' + '.' * 60 + '\n')
        if melhor_passado.count(g.somos[0].nota) >= max_wait_4_new_fitness:
            break
    return g


if __name__ == '__main__':
    freeze_support()
    populacao = População(entrada[0], entrada[1], entrada[2], list(somos),
                          max_somos=maxi)

    populacao = iterar(populacao)

    pasta_resultados = 'Resultados obtidos em ' + str(datetime.now()) \
        .split('.')[0].replace(':', '_')
    os.mkdir(pasta_resultados)
    os.chdir(pasta_resultados)
    for contador, somo in enumerate(populacao.somos):
        with open('Organização {0} (Nota:{1:.2f}).txt'
                          .format(contador + 1, somo.nota), 'w') as saida:
            tools.relatorio(somo, entrada, f=saida)
