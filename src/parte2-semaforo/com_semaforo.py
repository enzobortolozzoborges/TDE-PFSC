import threading
import time

T = 8
M = 200000
contador = 0
sem = threading.Semaphore(1)

def incrementar():
    global contador
    for i in range(M):
        sem.acquire()
        try:
            contador = contador + 1
        finally:
            sem.release()

threads = []
inicio = time.perf_counter()

for _ in range(T):
    t = threading.Thread(target=incrementar)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

fim = time.perf_counter()

print(f"Esperado: {T * M}")
print(f"Obtido: {contador}")
print(f"Tempo: {fim - inicio:.4f}")
