import sys  
import argparse 

impares = []

# Defino el parser
parser = argparse.ArgumentParser()

#Agrego los argumentos
parser.add_argument("numero", type=int, help="el número de impares a obtener")

# Recuperamos los argumentos
args = parser.parse_args()
numero = int(args.numero)


# Validamos que el número sea positivo
if numero <= 0:
    sys.stderr.write("Error: el argumento debe ser un número mayor a cero.\n")
    sys.exit()

# Obtenemos los números impares y los agregamos a la lista "impares"
for i in range(1, numero + 1):
    if i % 2 != 0:
        impares.append(i)

# Escribimos la lista en la salida estándar
sys.stdout.write(str(impares) + '\n')
