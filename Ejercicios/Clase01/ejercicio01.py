import sys

impares = []

# Validar el argumento
try:
    numero = int(sys.argv[1])
except IndexError:
    print("Error: se requiere un argumento.")
    sys.exit()
except ValueError:
    print("Error: el argumento debe ser un número entero.")
    sys.exit()

# Validar que el numero sea positivo
if numero <= 0:
    print("Error: el argumento debe ser un número natural positivo.")
    sys.exit()

# Obetenemos los numero impares
for i in range(1, numero + 1):
    if i % 2 != 0:
        impares.append(i)

# Escribimos la lista en la salida estandar
sys.stdout.write(str(impares) + '\n')