import multiprocessing
from time import time
import numpy as np

def fibo(n):
    if n < 2:
        return n
    return fibo(n-1) + fibo(n-2)

class FiboWorker(multiprocessing.Process):
    def __init__(self, vector, start_index, end_index, result_queue):
        multiprocessing.Process.__init__(self)
        self.vector = vector
        self.start_index = start_index
        self.end_index = end_index
        self.result_queue = result_queue
    
    def run(self):
        for i in range(self.start_index, self.end_index):
            self.vector[i] = fibo(self.vector[i])
        self.result_queue.put((self.start_index, self.end_index, self.vector[self.start_index:self.end_index]))

def main():
    vector_length = 144
    initial_value = 33
    num_cpus = multiprocessing.cpu_count()
    
    # Inicializar el vector
    vector = np.full(vector_length, initial_value)
    
    print(f"Procesando un vector de longitud {vector_length} con valor inicial {initial_value}")
    print(f"Utilizando {num_cpus} CPUs")
    
    # Dividir el trabajo entre los CPUs disponibles
    chunk_size = vector_length // num_cpus
    processes = []
    result_queue = multiprocessing.Queue()
    
    ts = time()
    
    for i in range(num_cpus):
        start_index = i * chunk_size
        end_index = start_index + chunk_size if i < num_cpus - 1 else vector_length
        worker = FiboWorker(vector, start_index, end_index, result_queue)
        processes.append(worker)
        worker.start()
    
    # Recolectar resultados
    for _ in range(num_cpus):
        start, end, partial_result = result_queue.get()
        vector[start:end] = partial_result
    
    # Esperar a que todos los procesos terminen
    for process in processes:
        process.join()
    
    print(f"Tiempo total de ejecución: {time() - ts:.2f} segundos")
    print("Primeros 10 elementos del vector procesado:", vector[:10])
    print("Últimos 10 elementos del vector procesado:", vector[-10:])

if __name__ == "__main__":
    main()