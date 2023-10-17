import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import socket
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

cliente = None
conexion_iniciada = False
estado_conexion = None

def iniciar_conexion():
    global cliente, conexion_iniciada
    if not conexion_iniciada:
        cliente = socket.socket()
        cliente.connect(("127.0.0.1", 5000))
        conexion_iniciada = True
        estado_conexion.set("Conexión iniciada")
    else:
        estado_conexion.set("Conexión ya iniciada")

def cerrar_conexion():
    global cliente, conexion_iniciada
    if cliente:
        cliente.close()
        conexion_iniciada = False
        estado_conexion.set("Conexión cerrada")

def cargar_archivo():
    ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")])
    if ruta_archivo:
        with open(ruta_archivo, 'r') as archivo:
            contenido = archivo.read()
            entrada_senal.delete(0, tk.END)  # Borrar contenido actual de la entrada
            entrada_senal.insert(0, contenido)  # Insertar contenido del archivo en la entrada

def enviar_senal():
    senal = entrada_senal.get()
    print(senal)
    ventana = entrada_ventana.get()

    # Combinar señal y ventana en un solo mensaje, separados por una coma
    mensaje = f"{senal} {ventana}"

    # Enviar señal y ventana al servidor
    cliente.send(mensaje.encode('utf-8'))
    print(f"Señal y ventana enviadas")

    # Recibir la señal suavizada del servidor
    senal_suavizada = cliente.recv(1024).decode('utf-8')
    
    # Mostrar la señal suavizada en la interfaz gráfica
    resultado.config(state=tk.NORMAL)
    resultado.delete('1.0', tk.END)
    resultado.insert(tk.END, senal_suavizada)
    resultado.config(state=tk.DISABLED)

    # Mostrar las señales gráficamente en una nueva ventana
    mostrar_grafica(senal, senal_suavizada)

def mostrar_grafica(senal, senal_suavizada):
    senal = list(map(float, senal.split(',')))
    senal_suavizada = list(map(float, senal_suavizada.split(',')))

    # Crear una nueva ventana para mostrar las gráficas
    ventana_graficas = tk.Toplevel(root)
    ventana_graficas.title("Gráficas")

    # Graficar señales
    fig, ax = plt.subplots(2, 1, figsize=(8, 6))

    # Señal original
    ax[0].plot(senal, label='Señal Original')
    ax[0].legend()

    # Señal suavizada
    ax[1].plot(senal_suavizada, label='Señal Suavizada', color='orange')
    ax[1].legend()

    # Agregar las gráficas a la ventana
    canvas = FigureCanvasTkAgg(fig, master=ventana_graficas)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Crear la ventana principal
root = tk.Tk()
root.title("Cliente")

# Etiqueta y entrada para la señal
label_senal = ttk.Label(root, text="Ingrese la señal (separada por comas) o cargue un archivo:")
label_senal.pack()

entrada_senal = ttk.Entry(root)
entrada_senal.pack()

# Botón para cargar archivo
boton_cargar = ttk.Button(root, text="Cargar Archivo", command=cargar_archivo)
boton_cargar.pack()

# Etiqueta y entrada para el tamaño de la ventana
label_ventana = ttk.Label(root, text="Tamaño de la ventana:")
label_ventana.pack()

entrada_ventana = ttk.Entry(root)
entrada_ventana.pack()

# Botón para enviar la señal al servidor
boton_enviar = ttk.Button(root, text="Enviar Señal", command=enviar_senal)
boton_enviar.pack()

# Resultado de la señal suavizada
label_resultado = ttk.Label(root, text="Señal Suavizada:")
label_resultado.pack()

resultado = tk.Text(root, width=40, height=10, state=tk.DISABLED)
resultado.pack()

# Botón para iniciar la conexión
boton_iniciar = ttk.Button(root, text="Iniciar Conexión", command=iniciar_conexion)
boton_iniciar.pack()

# Botón para cerrar la conexión
boton_cerrar = ttk.Button(root, text="Cerrar Conexión", command=cerrar_conexion)
boton_cerrar.pack()

# Etiqueta para mostrar estado de la conexión
estado_conexion = tk.StringVar()
etiqueta_estado = ttk.Label(root, textvariable=estado_conexion)
etiqueta_estado.pack()

# Iniciar la aplicación
root.mainloop()