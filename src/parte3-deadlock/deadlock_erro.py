import datetime
import threading
import time

lock_a = threading.Lock()
lock_b = threading.Lock()

def tarefa_1():
    print("T1: tentando lock A")
    with lock_a:
        print("T1: conseguiu lock A. aguardando")
        time.sleep(0.05)
        print("T1: tentando lock B")
        with lock_b:
            print("T1: finalizou")

def tarefa_2():
    print("T2: tentando lock B")
    with lock_b:
        print("T2: conseguiu lock B. aguardando")
        time.sleep(0.05)
        print("T2: tentando Lock A")
        with lock_a:
            print("T2: finalizou")

t1 = threading.Thread(target=tarefa_1, name="Thread-1")
t2 = threading.Thread(target=tarefa_2, name="Thread-2")

t1.start()
t2.start()

t1.join(timeout=2)
t2.join(timeout=2)

if t1.is_alive() or t2.is_alive():
    print("\nfinalizado com deadlock, trava")
    print("Threads bloqueadas:", threading.enumerate())