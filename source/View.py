import tkinter as tk
from tkinter import ttk, messagebox,PhotoImage,Label, Canvas
import threading
from PIL import ImageTk, Image
import os
from IPC import Barberia
import time

class Main:

    def __init__(self):
        self.hiloSimulation = threading.Thread()
        self.cantidad = 0
        self.barberia = Barberia(num_sillas=self.cantidad)
        self.create_components()
        self.create_window()
        self.add_components()
        self.create_images()
        self.barber_img('sources/images/sleep.png')
        self.activate = False
        #self.ventana.update()
        self.ventana.mainloop()

    def stopSimulation(self):
        self.barberia.stop()
        self.activate = False
        

    def startSimulation(self):
        self.activate = True
        self.cantidad = int(self.numeroSillas.get())
        print(self.cantidad)
        self.barberia.simular_barbero_dormilon(self.cantidad)
        self.hiloBarber = threading.Thread(target=self.barber_image, args=())
        self.hiloBarber.start()
        self.hiloChair = threading.Thread(target=self.chairsImages, args=())
        self.hiloChair.start()
        
        print(self.hiloSimulation.is_alive())
        #self.update_gui()


    def barber_image(self):
        while(self.activate):
            barber_is_sleep = self.barberia.get_sleep() 
            if barber_is_sleep:
                self.update_barber('sources/images/sleep.png')
            else:
                #print("Nooooo_________________________I_________")
                self.update_barber('sources/images/barberWakeup.png')
        # Actualizar el tamaño del área desplazable del canvas

    def chairsImages(self):
        while(self.activate):
            x = 0
            y = 0 
            sala_espera = self.barberia.get_list()
            if sala_espera == 0:
                for i in range(self.cantidad):
                    self.canvas.create_image(x, y, anchor='nw', image=self.silla_imag)
                    x += 80
                    if(x == 400):
                        x = 0
                        y += 80
            elif sala_espera > 0:
                if sala_espera == self.cantidad:
                    for i in range(self.cantidad):
                        self.canvas.create_image(x,y, anchor='nw', image=self.esperando_imag)
                        self.canvas.image = self.silla_imag
                        x += 80
                        if(x == 400):
                            x = 0
                            y += 80
            if 0 < sala_espera < self.cantidad:
                libres = self.cantidad - sala_espera
                for i in range(self.cantidad):
                    if i >= (self.cantidad - libres):
                       self.canvas.create_image(x, y, anchor='nw', image=self.silla_imag)
                       x += 80
                       if(x == 400):
                            x = 0
                            y += 80
                    else:
                       self.canvas.create_image(x, y, anchor='nw', image=self.esperando_imag)
                       x += 80
                    if(x == 400):
                        x = 0
                        y += 80

    def create_components(self):
        self.titleWindow = 'Sleepy barber'
        self.colorFondo = '#FFFFFF'
        self.colorFuentePrincipal = '#000000'
        self.colorEntry='#F5F5F5'
        self.mensajeHora='Reloj Sistema:'
        self.mensajeTSimulacion = 'Tiempo de simulacion'
        self.mensajeEstadoCpu='Estado CPU: '
        self.mensajeColaProcesos = 'Cola de Procesos en:'
        self.fuenteTitulo =('Mixed',30)
        self.fuentePrincipal =('Mixed,20')
        self.mensajeTablaProcesos='Cola de procesos: '
        self.list_length_process = [3, 5, 10]


    def create_window(self):
        self.ventana = tk.Tk()
        self.ventana.geometry("1000x500")
        self.ventana.title(self.titleWindow)
        self.ventana.resizable(0,0)
        self.ventana.config(bg=self.colorFondo)

        self.ventana.rowconfigure(0, weight=0)
        self.ventana.rowconfigure(1, weight=1)
        self.ventana.rowconfigure(2, weight=1)
        self.ventana.rowconfigure(3, weight=1)
        self.ventana.rowconfigure(4, weight=1)
        self.ventana.rowconfigure(5, weight=1)
        self.ventana.rowconfigure(6, weight=1)
        self.ventana.rowconfigure(7, weight=1)
        self.ventana.rowconfigure(8, weight=1)

        self.ventana.columnconfigure(0, weight=1)
        for i in range(1, 14):
            self.ventana.columnconfigure(i, weight=1)

    def add_components(self):
        self.labelTitulo1=tk.Label(self.ventana,text=self.titleWindow, bg=self.colorFondo, fg=self.colorFuentePrincipal, font=self.fuenteTitulo)
        self.labelTitulo1.grid(row=0, column=1, columnspan=5)

        #Separador
        self.separador=ttk.Separator(self.ventana,orient='horizontal')
        self.separador.grid(row=0, column=0, sticky='SWE', columnspan=14)
        self.separador2=ttk.Separator(self.ventana,orient='vertical')
        self.separador2.grid(row=1, column=2, sticky='NS', rowspan=5)
        self.separador3=ttk.Separator(self.ventana,orient='vertical')
        self.separador3.grid(row=1, column=9, sticky='NS', rowspan=5)
        self.separador4=ttk.Separator(self.ventana,orient='horizontal')
        self.separador4.grid(row=5, column=0, sticky='SWE', columnspan=14)

        #numero de sillas
        self.labelEntrySimulacion=tk.Label(self.ventana,text="Numero de sillas: ",border=0, bg=self.colorFondo, fg=self.colorFuentePrincipal, font=('Mixed',15))
        self.labelEntrySimulacion.grid(row=7, column=0, sticky='E', columnspan=2)
        self.numeroSillas = tk.Entry(self.ventana, fg=self.colorFuentePrincipal, font=('Mixed',15))
        self.numeroSillas.grid(row=7, column=2, sticky='E')
        self.imageButtonSimulacion = tk.PhotoImage(file='sources/images/play.png')
        self.imageButtonStopSimulacion = tk.PhotoImage(file='sources/images/stop.png')
        self.bottomStarSimulacion = tk.Button(self.ventana, image=self.imageButtonSimulacion, bd=0, bg=self.colorFondo, command= self.startSimulation)
        self.bottomStarSimulacion.grid(row=7, column=3, sticky='WE')
        self.bottomStopSimulacion = tk.Button(self.ventana, image=self.imageButtonStopSimulacion, bd=0, bg=self.colorFondo, command= self.stopSimulation)
        self.bottomStopSimulacion.grid(row=7, column=4, sticky='WE')

    def create_images(self):
        self.imagen_silla = Image.open('sources/images/silla.png')
        self.imagen_silla = self.imagen_silla.resize((80, 80)) 
        self.silla_imag = ImageTk.PhotoImage(self.imagen_silla)
        self.imagen_esperando = Image.open('sources/images/esperandojpg.png')
        self.imagen_esperando = self.imagen_esperando.resize((80, 80)) 
        self.esperando_imag = ImageTk.PhotoImage(self.imagen_esperando)
        self.canvas = Canvas(self.ventana, width=400, height=320)
        self.canvas.grid(row=2, column=0,sticky='E', columnspan=2)
        self.canvas.config(bg='white')
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))


    def update_barber(self, path):
        imagen = Image.open(path)
        imagen = imagen.resize((200, 300)) 
        photo = ImageTk.PhotoImage(imagen)  # Convertir a PhotoImage
        self.sleepBarber.configure(image=photo)
        self.sleepBarber.image = photo  # Actualizar referencia
  
    #Barbero
    # Cargar la imagen
    def barber_img(self, path):
        imagen = Image.open(path)
        imagen = imagen.resize((200, 300)) 
        self.sleepBarberImage = ImageTk.PhotoImage(imagen)
        self.sleepBarber = tk.Label(self.ventana, image=self.sleepBarberImage)
        self.sleepBarber.config(bg='white')
        self.sleepBarber.grid(row=2, column=2,sticky='E', columnspan=6)

    def update_gui(self):
        self.crear_imagenes()
        self.ventana.after(500, self.update_gui)


# Ejecutar el bucle principal de la aplicación
main = Main()



