from threading import Thread
from threading import Semaphore
import time
import random

num_filosofos = 5

garfos = [Semaphore(1) for i in range(num_filosofos)]
status = ["Pensando" for i in range (num_filosofos)]

def filosofo(i):
    print("Filosofo", i, "está", status[i])
    time.sleep(0.5)
    print("Filosofo", i, "está com fome")

    if i == num_filosofos - 1:
        garfos[(i + 1) % num_filosofos].acquire()
        garfos[i].acquire()
    else:
        garfos[i].acquire()
        garfos[(i + 1) % num_filosofos].acquire()

    print("Filosofo", i, "está comendo")
    time.sleep(0.5)

    print("Filósofo", i, "terminou de comer e está pensando")

    if i == num_filosofos - 1:
        garfos[i].release()
        garfos[(i + 1) % num_filosofos].release()
    else:
        garfos[(i + 1) % num_filosofos].release()
        garfos[i].release()

total = [Thread(target=filosofo, args=[i]) for i in range (num_filosofos)]
random.shuffle(total)

for i in total:
    i.start()

for i in total:
    i.join()