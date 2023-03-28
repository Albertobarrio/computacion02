import sys
import argparse

# Defino el parser
parser = argparse.ArgumentParser(description='Imprime el texto ingresado n veces')

#Agrego los argumentos
parser.add_argument('texto', type=str, help='Cadena de texto a imprimir')
parser.add_argument('numero', type=int, help='Número de veces que se debe imprimir el texto')

# Recuperamos los argumentos
args = parser.parse_args()

texto = args.texto
numero = args.numero

# Escribimos el texto en la salida estandar
sys.stdout.write( (texto + '\n') * numero )   