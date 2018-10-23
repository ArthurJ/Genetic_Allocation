# Genetic_Allocation

A schedule generator which aims at maximizing satisfaction among its users, matching their availability with an institution’s needs. Users apply grades to available spots on a timetable to express their willing to work at a specific time. Then, the generator uses the grades applied by the users to create timetable suggestions using genetic algorithms, thus building a sustainable schedule which conciliates professionals’ and institutions’ best interests.

----------------------------------------------------------------------------------------------------------

Organização de horários de escala baseado em na preferência dos profissionais, com limitações de local.

Esse projeto nasceu da necessidade de organizar a escala de horários de professores na UFABC para uma disciplina que será lecionada para multiplas salas, em multiplos horários, em mais de um campus num mesmo quadrimestre.

O input do projeto é um arquivo ".csv" com separação por ";".
Esse arquivo contém uma matriz (eixo x = Nome dos professores, eixo y = Horários/Campus).
A matriz contém valores (0-10) onde 0 implica na impossibilidade do professor lecionar a disciplina naquele horário, e valores de 1-10 mostram a intensidade com que o professor quer o determinado horário.

O programa usa um algoritmo genético para criar exemplos de organização que tentam satisfazer ao máximo todos, ou a maior parte, dos professores.

O programa pode ser usado para criar escalas de horários em qualquer contexto.

Em caso de dúvidas, entre em contato: azrael.zila@gmail.com
