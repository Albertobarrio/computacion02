import argparse
import socketserver
from http.server import SimpleHTTPRequestHandler
from PIL import Image
import io
import threading
import multiprocessing
import socket
import os

# Variable global para almacenar el puerto del servidor secundario
SCALE_SERVER_PORT = 8081  # Puerto predeterminado para el servidor de escalado
SCALE_FACTOR = 0.5  # Escala predeterminada

def process_image(lock, image_data):
    try:
        lock.acquire()
        original_image = Image.open(io.BytesIO(image_data))
        grayscale_image = original_image.convert('L')

        buffered = io.BytesIO()
        grayscale_image.save(buffered, format="JPEG")
        processed_image = buffered.getvalue()
    finally:
        lock.release()

    return processed_image

def scale_image(factor, image_data):
    try:
        original_image = Image.open(io.BytesIO(image_data))
        width, height = original_image.size
        new_width = int(width * factor)
        new_height = int(height * factor)
        scaled_image = original_image.resize((new_width, new_height))

        buffered = io.BytesIO()
        scaled_image.save(buffered, format="JPEG")
        scaled_image_data = buffered.getvalue()

        return scaled_image_data
    except Exception as e:
        print(f"Error al escalar la imagen: {e}")
        return None

def run_server(ip, port, lock):
    class CustomHandler(SimpleHTTPRequestHandler):
        def do_POST(self):
            if self.path == '/upload':
                try:
                    content_length = int(self.headers['Content-Length'])
                    image_data = self.rfile.read(content_length)

                    processed_image = process_image(lock, image_data)

                    # Enviar la imagen procesada al cliente
                    self.send_response(200)
                    self.send_header('Content-type', 'image/jpeg')
                    self.send_header('Content-length', len(processed_image))
                    self.end_headers()
                    self.wfile.write(processed_image)

                    # Escalar la imagen en el servidor secundario
                    scale_image_on_secondary_server(self.path, processed_image)

                except Exception as e:
                    print(f"Error al procesar la imagen: {e}")
                    self.send_error(500, "Internal Server Error")
            else:
                super().do_POST()

    handler = CustomHandler
    server = socketserver.ThreadingTCPServer((ip, port), handler)

    print(f"Servidor principal en http://{ip}:{port}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Servidor detenido")

def scale_image_on_secondary_server(path, image_data):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(('127.0.0.1', SCALE_SERVER_PORT))

            # Enviar la solicitud POST a /scale al servidor secundario
            sock.sendall(b'POST /scale HTTP/1.1\r\n')
            sock.sendall(f'Content-Length: {len(image_data)}\r\n'.encode())
            sock.sendall(f'Scale-Factor: {SCALE_FACTOR}\r\n'.encode())  # Use the global scale factor
            sock.sendall(b'Content-Type: image/jpeg\r\n\r\n')
            sock.sendall(image_data)

            # Leer la respuesta del servidor secundario
            response = b''
            while True:
                data = sock.recv(1024)
                if not data:
                    break
                response += data

            # Guardar la imagen escalada en el directorio actual
            scaled_image_path = os.path.join(os.getcwd(), 'imagen_escalada.jpg')
            with open(scaled_image_path, 'wb') as scaled_image_file:
                scaled_image_file.write(response.split(b'\r\n\r\n', 1)[1])  # Write only image data

            # Imprimir la respuesta HTTP del servidor secundario
            print(f"La imagen escalada se guardo en: {scaled_image_path}")
    except Exception as e:
        print(f"Error escalando la imagen en el segundo servidor: {e}")

def run_scale_server(ip, port=SCALE_SERVER_PORT):
    class ScaleServerHandler(SimpleHTTPRequestHandler):
        def do_POST(self):
            try:
                if self.path == '/scale':
                    content_length = int(self.headers['Content-Length'])
                    image_data = self.rfile.read(content_length)

                    # Escalar la imagen según el factor proporcionado
                    scaled_image = scale_image(SCALE_FACTOR, image_data)

                    if scaled_image:
                        # Configurar la respuesta HTTP
                        self.send_response(200)
                        self.send_header('Content-type', 'image/jpeg')
                        self.send_header('Content-length', len(scaled_image))
                        self.end_headers()

                        # Enviar la imagen escalada al cliente
                        self.wfile.write(scaled_image)
                    else:
                        self.send_error(500, "Internal Server Error")
                else:
                    super().do_POST()
            except Exception as e:
                print(f"Error procesadon la request de escalado: {e}")
                self.send_error(500, "Internal Server Error")

    handler = ScaleServerHandler
    scale_server = socketserver.ThreadingTCPServer((ip, port), handler)

    print(f"Servidor de escalado en http://{ip}:{port}")

    try:
        scale_server.serve_forever()
    except KeyboardInterrupt:
        print("Servidor de escalado detenido")

def parse_args():
    parser = argparse.ArgumentParser(description='Tp2 - Procesa imágenes')
    parser.add_argument('-i', '--ip', required=True, help='Dirección de escucha')
    parser.add_argument('-p', '--port', type=int, required=True, help='Puerto de escucha')

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    ip_address = args.ip
    port = args.port

    # Crear un Lock para el mecanismo de sincronización
    lock = threading.Lock()

    # Crear un proceso para ejecutar el servidor de escala
    scale_server_process = multiprocessing.Process(target=run_scale_server, args=('127.0.0.1',))
    scale_server_process.start()

    run_server(ip_address, port, lock)
