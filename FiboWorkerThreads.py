from threading import Thread
from time import time
import numpy as np
import multiprocessing
import sys

def fibo(n):
    if n < 2:
        return n
    return fibo(n-1) + fibo(n-2)

class FiboWorker(Thread):
    def __init__(self, vector, start_index, end_index):
        Thread.__init__(self)
        self.vector = vector
        self.start_index = start_index
        self.end_index = end_index

    def run(self):
        for i in range(self.start_index, self.end_index):
            self.vector[i] = fibo(self.vector[i])
        print(f"[{self.name}] Procesado desde {self.start_index} hasta {self.end_index-1}")

def main():
    vector_length = 144
    initial_value = 33
    
    if len(sys.argv) > 1:
        initial_value = int(sys.argv[1])

    num_cpus = multiprocessing.cpu_count()
    
    # Inicializar el vector
    vector = np.full(vector_length, initial_value)

    print(f"Procesando un vector de longitud {vector_length} con valor inicial {initial_value}")
    print(f"Utilizando {num_cpus} hilos")

    # Dividir el trabajo entre los hilos
    chunk_size = vector_length // num_cpus
    hilos = []

    ts = time()

    for x in range(num_cpus):
        start_index = x * chunk_size
        end_index = start_index + chunk_size if x < num_cpus - 1 else vector_length
        print(f"Trabajador {x} comienza")
        worker = FiboWorker(vector, start_index, end_index)
        worker.start()
        hilos.append(worker)

    for x, hilo in enumerate(hilos):
        print(f"Esperando por trabajador {x}")
        hilo.join()

    print(f"Tiempo total de ejecución: {time() - ts:.2f} segundos")
    print("Primeros 10 elementos del vector procesado:", vector[:10])
    print("Últimos 10 elementos del vector procesado:", vector[-10:])

if __name__ == "__main__":
    main()
    