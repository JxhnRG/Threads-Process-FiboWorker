from time import time
import numpy as np
import sys

def fibo(n):
    if n < 2:
        return n
    return fibo(n-1) + fibo(n-2)

def main():
    vector_length = 144
    initial_value = 33
    
    if len(sys.argv) > 1:
        initial_value = int(sys.argv[1])

    # Inicializar el vector
    vector = np.full(vector_length, initial_value)

    print(f"Procesando un vector de longitud {vector_length} con valor inicial {initial_value}")
    print("Ejecutando de forma secuencial")

    ts = time()

    # Procesar el vector secuencialmente
    for i in range(vector_length):
        vector[i] = fibo(vector[i])
        print(f"Procesado elemento {i}")

    print(f"Tiempo total de ejecución: {time() - ts:.2f} segundos")
    print("Primeros 10 elementos del vector procesado:", vector[:10])
    print("Últimos 10 elementos del vector procesado:", vector[-10:])

if __name__ == "__main__":
    main()