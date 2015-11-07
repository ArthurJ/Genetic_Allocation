# Genetic_Allocation
Organização de horários de escala baseado em na preferência dos profissionais, com limitações de local.

Esse projeto nasceu da necessidade de organizar a escala de horários de professores na UFABC para uma disciplina que será lecionado para multiplas salas, em multiplos horários, em mais de um campus num mesmo quadrimestre.

O input do projeto é um arquivo ".csv" com separação por ";".
Esse arquivo ontem uma matriz (eixo x = Nome dos professores, eixo y = Horários/Campus).
A matriz contem valores (0-10) onde 0 implica na impossibilidade do professor lecionar a matéria, e valores de 1-10 mostrando a intensidade com que o professor quer o determinado horário.

O programa usa um algoritmo genético para criar exemplos de organização que tentam satisfazer ao máximo todos, ou a maior parte, dos professores.

O programa pode ser usado para criar escalas de horários em qualquer contexto.

Em caso de dúvidas, entre em contato.
azrael.zila@gmail.com
