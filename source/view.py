import tkinter as tk
from tkinter import ttk, messagebox,PhotoImage,Label, Canvas
from PIL import ImageTk, Image
import os
from IPC import colaClientes, Barberia
import threading

def startSimulation():
    barberia = Barberia(int(numeroSillas.get()))
    hiloSimulation = threading.Thread(target=barberia.start)
    hiloSimulation.start()

def crear_imagenes():
    # Obtener la cantidad de veces que se desea mostrar la imagen
    cantidad = int(numeroSillas.get())
    for i in range(cantidad):
        canvas.create_image(0, 12 + i * 50, anchor='nw', image=silla_imag)
        # Guardar una referencia a la imagen en el objeto
        canvas.image = silla_imag
    # Actualizar el tamaño del área desplazable del canvas
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))


titleWindow = 'Sleepy barber'
colorFondo = '#FFFFFF'
colorFuentePrincipal = '#000000'
colorEntry='#F5F5F5'
mensajeHora='Reloj Sistema:'
mensajeTSimulacion = 'Tiempo de simulacion'
mensajeEstadoCpu='Estado CPU: '
mensajeColaProcesos = 'Cola de Procesos en:'
fuenteTitulo =('Mixed',30)
fuentePrincipal =('Mixed,20')
mensajeTablaProcesos='Cola de procesos: '
list_length_process = [3, 5, 10]


# Crear la ventana principal
ventana = tk.Tk()
ventana.geometry("1000x500")
ventana.title(titleWindow)
ventana.resizable(0,0)
ventana.config(bg=colorFondo)

#Configurar el grid
ventana.rowconfigure(0, weight=0)
ventana.rowconfigure(1, weight=1)
ventana.rowconfigure(2, weight=1)
ventana.rowconfigure(3, weight=1)
ventana.rowconfigure(4, weight=1)
ventana.rowconfigure(5, weight=1)
ventana.rowconfigure(6, weight=1)
ventana.rowconfigure(7, weight=1)
ventana.rowconfigure(8, weight=1)

ventana.columnconfigure(0, weight=1)
for i in range(1, 14):
    ventana.columnconfigure(i, weight=1)

#Componente Titulo Principal
labelTitulo1=tk.Label(ventana,text=titleWindow, bg=colorFondo, fg=colorFuentePrincipal, font=fuenteTitulo)
labelTitulo1.grid(row=0, column=1, columnspan=5)

#Separador
separador=ttk.Separator(ventana,orient='horizontal')
separador.grid(row=0, column=0, sticky='SWE', columnspan=14)
separador2=ttk.Separator(ventana,orient='vertical')
separador2.grid(row=1, column=2, sticky='NS', rowspan=5)
separador3=ttk.Separator(ventana,orient='vertical')
separador3.grid(row=1, column=9, sticky='NS', rowspan=5)
separador4=ttk.Separator(ventana,orient='horizontal')
separador4.grid(row=5, column=0, sticky='SWE', columnspan=14)

#numero de sillas
labelEntrySimulacion=tk.Label(ventana,text="Numero de sillas: ",border=0, bg=colorFondo, fg=colorFuentePrincipal, font=('Mixed',15))
labelEntrySimulacion.grid(row=7, column=0, sticky='E', columnspan=2)
numeroSillas = tk.Entry(ventana, fg=colorFuentePrincipal, font=('Mixed',15))
numeroSillas.grid(row=7, column=2, sticky='E')
imageButtonSimulacion = tk.PhotoImage(file='C:/Users/casti/Documents/SO/proyectos/IPC_BarberoDormilon/sources/images/play.png')
bottomStarSimulacion = tk.Button(ventana, image=imageButtonSimulacion, bd=0, bg=colorFondo, command= crear_imagenes)
bottomStarSimulacion.grid(row=7, column=3, sticky='WE')

#sillas
scrollbar = ttk.Scrollbar(ventana)
scrollbar.grid(row=2, column=3, sticky='E',rowspan=3, columnspan=2)
imagen_silla = Image.open('C:/Users/casti/Documents/SO/proyectos/IPC_BarberoDormilon/sources/images/silla.png')
imagen_silla = imagen_silla.resize((50, 50)) 
silla_imag = ImageTk.PhotoImage(imagen_silla)
canvas = Canvas(ventana, width=400, height=300)
canvas.grid(row=2, column=0,sticky='E', columnspan=2)
canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=canvas.yview)
canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

#Barbero
# Cargar la imagen
imagen = Image.open('C:/Users/casti/Documents/SO/proyectos/IPC_BarberoDormilon/sources/images/sleep.png')
imagen = imagen.resize((200, 300)) 
sleepBarberImage = ImageTk.PhotoImage(imagen)
sleepBarber = tk.Label(ventana, image=sleepBarberImage)
sleepBarber.config(bg='white')
sleepBarber.grid(row=2, column=2,sticky='E', columnspan=6)


# Ejecutar el bucle principal de la aplicación
ventana.mainloop()