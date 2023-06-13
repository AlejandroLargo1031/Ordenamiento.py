import os
import shutil
from tkinter import *
from tkinter import filedialog, messagebox

# Función para crear la estructura inicial de carpetas
def crear_estructura_carpeta():
    meses = [
        'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
        'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
    ]
    for mes in meses:
        carpeta_mes = os.path.join(carpeta_principal, mes)
        os.makedirs(carpeta_mes, exist_ok=True)

# Función para ordenar los archivos en las carpetas correspondientes
def ordenar_archivos():
    archivos_txt = [f for f in os.listdir(carpeta_principal) if f.endswith('.txt')]
    for archivo in archivos_txt:
        fecha = obtener_fecha_archivo(archivo)
        if fecha:
            carpeta_destino = obtener_carpeta_destino(fecha)
            ruta_archivo = os.path.join(carpeta_principal, archivo)
            shutil.move(ruta_archivo, carpeta_destino)

# Función para obtener la fecha del nombre de un archivo
def obtener_fecha_archivo(archivo):
    partes_nombre = os.path.splitext(archivo)[0].split('_')
    if len(partes_nombre) == 2:
        return partes_nombre[1]
    return None

# Función para obtener la carpeta de destino según la fecha
def obtener_carpeta_destino(fecha):
    partes_fecha = fecha.split('-')
    if len(partes_fecha) == 3:
        mes = int(partes_fecha[1])
        return os.path.join(carpeta_principal, meses[mes - 1])
    return carpeta_principal

# Función para crear un nuevo archivo y ordenarlo
def crear_archivo():
    nombre_archivo = entry_nombre.get()
    contenido_archivo = entry_contenido.get('1.0', END)

    if not nombre_archivo or not contenido_archivo:
        messagebox.showwarning("Advertencia", "Debe proporcionar un nombre y contenido para el archivo.")
        return

    fecha = obtener_fecha_archivo(nombre_archivo)
    if not fecha:
        messagebox.showwarning("Advertencia", "El nombre del archivo no contiene una fecha válida.")
        return

    ruta_archivo = os.path.join(carpeta_principal, nombre_archivo)
    with open(ruta_archivo, 'w') as archivo:
        archivo.write(contenido_archivo)

    ordenar_archivos()

    messagebox.showinfo("Archivo creado", "El archivo se ha creado y ordenado correctamente.")

# Función para abrir un archivo existente
def abrir_archivo():
    ruta_archivo = filedialog.askopenfilename(initialdir=carpeta_principal, filetypes=[('Archivos de texto', '*.txt')])
    if ruta_archivo:
        with open(ruta_archivo, 'r') as archivo:
            contenido_archivo = archivo.read()
        entry_nombre.delete(0, END)
        entry_nombre.insert(0, os.path.basename(ruta_archivo))
        entry_contenido.delete('1.0', END)
        entry_contenido.insert('1.0', contenido_archivo)

# Función para eliminar un archivo existente
def eliminar_archivo():
    nombre_archivo = entry_nombre.get()
    if not nombre_archivo:
        messagebox.showwarning("Advertencia", "Debe proporcionar un nombre de archivo válido.")
        return

    archivo_encontrado = False  # Variable para indicar si se encontró el archivo

    for root, dirs, files in os.walk(carpeta_principal):
        if nombre_archivo in files:
            ruta_archivo = os.path.join(root, nombre_archivo)
            os.remove(ruta_archivo)
            archivo_encontrado = True
            break  # Se encontró el archivo, se sale del bucle

    if archivo_encontrado:
        messagebox.showinfo("Archivo eliminado", "El archivo se ha eliminado correctamente.")
        entry_contenido.delete('1.0', END)
        ordenar_archivos()
    else:
        messagebox.showwarning("Advertencia", "El archivo no existe.")

# Configuración inicial de la interfaz gráfica
root = Tk()
root.title("Ordenar archivos .txt por fecha")

# Carpeta principal donde se almacenarán los archivos
carpeta_principal = "Archivos"
os.makedirs(carpeta_principal, exist_ok=True)
crear_estructura_carpeta()

# Lista de meses del año
meses = [
    'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
]

# Etiquetas y campos de entrada
label_nombre = Label(root, text="Nombre del archivo:")
label_nombre.pack()
entry_nombre = Entry(root)
entry_nombre.pack()

label_contenido = Label(root, text="Contenido:")
label_contenido.pack()
entry_contenido = Text(root, height=5, width=30)
entry_contenido.pack()

# Botones
frame_botones = Frame(root)
frame_botones.pack()

boton_crear = Button(frame_botones, text="Crear archivo", command=crear_archivo)
boton_crear.grid(row=0, column=0, padx=5, pady=5)

boton_abrir = Button(frame_botones, text="Abrir archivo", command=abrir_archivo)
boton_abrir.grid(row=0, column=1, padx=5, pady=5)

boton_eliminar = Button(frame_botones, text="Eliminar archivo", command=eliminar_archivo)
boton_eliminar.grid(row=0, column=2, padx=5, pady=5)

# Iniciar la interfaz gráfica
root.mainloop()
