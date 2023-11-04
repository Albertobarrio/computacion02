import argparse
import os
import sys
import time

def invertir_linea(linea, w):
    w.write(linea[::-1])

# Test
def procesar_archivo(archivo):
    procesos = []
    for linea in archivo:
        r, w = os.pipe()
        pid = os.fork()
        if pid == 0:  # Proceso hijo
            os.close(r)
            w = os.fdopen(w, 'w')
            invertir_linea(linea, w)
            w.close()
            os._exit(0)
        else:  # Proceso padre
            os.close(w)
            r = os.fdopen(r)
            procesos.append((pid, r))

    # Esperar a que terminen los hijos
    for pid, r in procesos:
        os.waitpid(pid, 0)
        print(r.read())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Inversor',
                                     description='Invierte un archivo de texto',
                                     epilog='Trabajo Practico Obligatorio')

    parser.add_argument('-f',
                        '--file',
                        action='store',
                        required=True,
                        help='Archivo a invertir')

    args = parser.parse_args()

    try:
        with open(args.file, 'r') as archivo:
            procesar_archivo(archivo)
    except FileNotFoundError:
        print(f"El archivo '{args.archivo}' no existe.")
    except IsADirectoryError:
        print(f"'{args.archivo}' es un directorio.")
    except PermissionError:
        print(f"No se tienen permisos para abrir el archivo '{args.archivo}'.")
