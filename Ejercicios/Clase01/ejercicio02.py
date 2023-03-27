import sys

# Validamos que se ingresen dos argumentos 
if len(sys.argv) != 3:
    sys.stderr.write('Se deben pasar dos argumentos una cadena de texto y un número\n')
    sys.exit(1)

# Obtenemos los argumentos
texto = sys.argv[1]
numero = sys.argv[2]


# Comprobamos que el segundo argumento sea un número entero
try:
    numero = int(numero)
except ValueError:
    sys.stderr.write('El segundo argumento debe ser un número entero\n')
    sys.exit(1)

# Escribimos el texto en la salida estandar
sys.stdout.write( texto * numero + '\n')   