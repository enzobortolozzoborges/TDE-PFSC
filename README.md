# TDE-PFSC
Davi Batista & Enzo Bortolozzo Borges


# Video Youtube

https://youtu.be/AecwWq8B_tY

# *-Parte 1 - Filosofos*

No jantar, cada filosofo precisa de 2 talheres para comer, e cada talher é dividido com um vizinho, no ingênuo todos pegam o garfo da esquerda primeiro, e depois o da direita, se todos ficarem com fome juntos pegam primeiro o garfo da esquerda, e ficam esperando o da direita, que ja esta ocupado, a solução foi fazer com que o filosofo 4 pegue primeiro o garfo 0 antes do 4, assim por nenhum filosofo segurar o garfo de indice maior esperando o de menor, sempre tem alguem com dois garfos.

Versão com deadlock: src/parte 1-filosofos/problema com deadlock.py

Versão sem deadlock: src/parte 1-filosofos/problema sem deadlock.py

![Diagrama.png](src/parte 1-filosofos/Diagrama.png)

# *-Parte 2 - Semaforo*
### Tabela de Resultados
 
| Versão       | Execução | Valor Esperado | Valor Obtido | Tempo (s) |
|--------------|:--------:|---------------:|-------------:|----------:|
| Sem Semáforo |    1     |        1600000 |       200280 |    1.1446 |
| Sem Semáforo |    2     |        1600000 |       200640 |    1.1538 |
| Sem Semáforo |    3     |        1600000 |       200420 |    1.1586 |
| Com Semáforo |    1     |        1600000 |      1600000 |    2.2008 |
| Com Semáforo |    2     |        1600000 |      1600000 |    2.2029 |
| Com Semáforo |    3     |        1600000 |      1600000 |    1.8701 |


Por que a versão sem sincronização perde incrementos
No sem_semaforo.py, o incremento acontece em duas etapas: primeiro a thread lê o valor (temp = contador) e depois grava contador = temp + 1. Entre essas duas linhas, o time.sleep(0) força uma troca de contexto, a thread para com um valor antigo guardado em temp e as outras threads continuam incrementando o contador. Quando ela volta, grava temp + 1 por cima e perde tudo o que as outras fizeram nesse meio-tempo. Por isso o valor final fica abaixo do esperado.

Por que a versão com semáforo funciona
No com_semaforo.py usei um semáforo binário threading.Semaphore(1). Antes de mexer no contador, a thread chama sem.acquire(), e só libera no finally com sem.release(). Como o semáforo tem apenas 1 permissão, apenas uma thread por vez consegue entrar na seção. As outras ficam esperando, então não tem como duas threads lerem o mesmo valor e uma sobrescrever a outra.

Trade-off de desempenho
Sem o semáforo o tempo médio ficou em torno de 1,15s porque as 8 threads rodam sem esperar umas pelas outras. É mais rápido, mas o resultado sai errado, já com o semáforo o tempo subiu para cerca de 2s. Isso acontece por que o acesso ao contador passa a ser feito uma thread de cada vez, então elas ficam paradas na fila, e ainda tem o custo de fazer acquire e release 1.600.000 vezes. trocando velocidade por um resultado correto.

Visibilidade e ordem das operações
O semáforo garante a ordem das operações e impede acesso simultâneo. Quando uma thread faz release() e a próxima consegue fazer acquire(), tudo o que a primeira escreveu no contador já está visível para a segunda. A próxima thread sempre lê o valor atualizado.

# *-Parte 3 - deadlock*
O deadlock_erro.py reproduz o problema, e o deadlock_corrigido.py a solução. Os dois usam duas threads (Thread-1 e Thread-2) e dois locks (lock_a e lock_b).

(deadlock_erro.py)
A Thread-1 pega o lock_a, espera 50 ms e depois tenta pegar o lock_b. A Thread-2 faz o contrário: pega o lock_b, espera 50 ms e tenta pegar o lock_a. Os 50 ms servem para garantir que cada thread já esteja com o primeiro lock quando a outra for pedir o segundo.
Threading.enumerate() para listar as threads que ainda estavam vivas, assim, Thread-1 e a Thread-2 continuam travadas esperando uma pela outra:
```text
T1: tentando lock A
T1: conseguiu lock A. aguardando
T2: tentando lock B
T2: conseguiu lock B. aguardando
T1: tentando lock B
T2: tentando Lock A
finalizado com deadlock, trava
Threads bloqueadas: [<_MainThread(MainThread, started 18632)>, <Thread(Thread-1, started 6972)>, <Thread(Thread-2, started 1476)>]
```
Esse travamento acontece porque as quatro condições de Coffman aparecem ao mesmo tempo:
Exclusão mútua: cada lock só pode ficar com uma thread por vez.
Manter e esperar: cada thread continua segurando o lock enquanto espera o outro.
Não preempção: não se tira o lock de uma thread à força, nem o sistema operacional nem o Python. Só é liberado quando a própria thread sai do bloco with.
Espera circular: Thread-1 espera o lock_b, que está com a Thread-2, e a Thread-2 espera o lock_a. Uma depende da outra e nenhuma consegue avançar.

(deadlock_corrigido.py)
A correção foi definir uma ordem fixa para pegar os locks. tarefa_2 pega primeiro o lock_a e depois o lock_b, igual à tarefa_1.
Quebrando a 4ª condição de Coffman (espera circular). Como as duas threads começam pelo lock_a, a que chegar depois fica esperando o primeiro lock, sem estar segurando o lock_b. Assim a primeira thread consegue pegar o lock_b, termina e solta os dois locks. Aí a segunda thread continua normalmente.
```text
T1: tentando lock A
T1: conseguiu lock A. aguardando
T2: tentando Lock A
T1: tentando lock B
T1 finalizou
T2:conseguiu lock A. aguardando
T2: tentando lock B
T2 finalizou
Finalizou sem deadlock
```
