import socket
import numpy as np

def media_movil(senal, ventana):
    senal_suavizada = np.convolve(senal, np.ones(ventana)/ventana, mode='valid')
    return senal_suavizada

host = "127.0.0.1"
port = 5000

servidor = socket.socket()
servidor.bind((host, port))
servidor.listen(1)

print(f"Esperando conexiones en {host}:{port}...")

while True:
    cliente, direccion = servidor.accept()
    print(f"Conexión establecida desde {direccion}")

    while True:
        # Recibir señal y ventana desde el cliente
        mensaje = cliente.recv(4096).decode('utf-8')

        if not mensaje:
            break

        senal, ventana = mensaje.split(' ')
        senal = [float(x) for x in senal.split(',')]
        ventana = int(ventana)

        # Aplicar el filtro de media móvil
        senal_suavizada = media_movil(senal, ventana)

        # Enviar la señal suavizada de vuelta al cliente
        cliente.send(','.join(map(str, senal_suavizada)).encode('utf-8'))

    # Cerrar la conexión
    cliente.close()