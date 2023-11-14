# TP2 - Procesamiento de Imágenes

Este script en Python implementa un servidor HTTP que puede recibir imágenes, procesarlas a escala de grises y devolverlas al cliente. El procesamiento de imágenes se realiza en un proceso hijo utilizando la biblioteca Pillow (PIL).

## Requisitos

- Python 3
- Biblioteca Pillow (PIL)
  ```bash
  pip install pillow

## 1. Clona el Reporsitorio
git clone https://github.com/tu-usuario/tp2-imagenes.git
cd tp2-imagenes

## 2. Ejecuta el script con la dirección IP y el puerto deseados:
python tp2.py -i 127.0.0.1 -p 8080

## 3. En otra terminal, utiliza curl para enviar una imagen al servidor:

### 3.1 Para cambiar a ecala de grises y despues rescalar
curl -X POST -H "Content-Type: image/jpeg" --data-binary "@/ruta/a/la/imagen.jpg" http://127.0.0.1:8080/upload --output imagen_procesada.jpg

### 3.2 Para cambiar rescalar la imagen solamente
curl -X POST -H "Content-Type: image/jpeg" --data-binary "@/home/beto/paisaje.jpg"  http://127.0.0.1:8081/scale --output imagen_procesada.jpg

## 4. Verifica la consola del servidor para ver mensajes sobre la recepción y procesamiento de la imagen.

## Opciones de `curl`

- `--output -`: Envía la salida binaria directamente a la terminal.
- `--output imagen_procesada.jpg`: Guarda la imagen procesada en un archivo llamado `imagen_procesada.jpg`.



