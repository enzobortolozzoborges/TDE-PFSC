import threading
import time

T = 8
M = 200000
contador = 0

def incrementar():
    global contador
    for i in range(M):
        temp = contador
        if i % 10 == 0: 
            time.sleep(0)
        contador = temp + 1

threads = []
inicio = time.perf_counter()

for _ in range(T):
    t = threading.Thread(target=incrementar)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

fim = time.perf_counter()

print(f"Esperando: {T * M}")
print(f"Obtido: {contador}")
print(f"Tempo: {fim - inicio:.4f}")
