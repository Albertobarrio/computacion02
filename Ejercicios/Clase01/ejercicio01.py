import sys

impares = []

# Validar el argumento
try:
    numero = int(sys.argv[1])
except IndexError:
    sys.stderr.write("Error: se requiere un argumento.\n")
    sys.exit()
except ValueError:
    sys.stderr.write("Error: el argumento debe ser un número entero.\n")
    sys.exit()

# Validar que el numero sea positivo
if numero <= 0:
    sys.stderr.write("Error: el argumento debe ser un número natural positivo.\n")
    sys.exit()

# Obetenemos los numero impares
for i in range(1, numero + 1):
    if i % 2 != 0:
        impares.append(i)

# Escribimos la lista en la salida estandar
sys.stdout.write(str(impares) + '\n')