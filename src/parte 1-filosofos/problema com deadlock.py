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
    print("Filosofo", i, "Está com fome")
    garfos[i].acquire()
    garfos[(i+1) % num_filosofos].acquire()
    print("Filosofo", i, "está comendo")
    time.sleep(0.5)

    print("Filósofo", i, "terminou de comer e está pensando")

    garfos[i].release()
    garfos[(i+1) % num_filosofos].release()

total = [Thread(target=filosofo, args=[i]) for i in range (num_filosofos)]
random.shuffle(total)

for i in total:
    i.start()

for i in total:
    i.join()