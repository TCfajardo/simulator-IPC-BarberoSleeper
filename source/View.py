import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage, Label, Canvas
import threading
from PIL import ImageTk, Image
import os
from IPC import Barberia
import time
import matplotlib.pyplot as plt
import numpy as np

class Main:

    def __init__(self):
        """
        Initializes an instance of the class.

        """
        self.hiloSimulation = threading.Thread()
        self.cantidad = 0
        self.barberia = Barberia(num_sillas=self.cantidad)
        self.create_components()
        self.create_window()
        self.add_components()
        self.create_images()
        self.create_logs()
        self.barber_img('source\sources\images\sleep.png')
        self.activate = False
        # self.ventana.update()
        self.ventana.mainloop()

    def stopSimulation(self):
        """
        Stops the simulation.

        """
        self.barberia.stop()
        self.activate = False

    def startSimulation(self):
        """
        Starts the simulation.

        """
        self.activate = True
        try:
            self.cantidad = int(self.numeroSillas.get())
            self.barberia.simular_barbero_dormilon(self.cantidad)
            self.hiloBarber = threading.Thread(target=self.barber_image, args=())
            self.hiloBarber.start()
            self.hiloChair = threading.Thread(target=self.chairsImages, args=())
            self.hiloChair.start()
            self.hiloLogs = threading.Thread(target=self.create_logs, args=())
            self.hiloLogs.start()
            print(self.hiloSimulation.is_alive())
        except ValueError:
            messagebox.showerror("Error", "Ingrese un valor valido")
        # self.update_gui()

    def showInfo(self):
        """
        Displays information about the simulation.

        """
        text = "---Instrucciones---\n - Ingrese el numero de asientos totales en la sala de espera en el campo " \
               "requerido\n - Pulse en el boton de play\n - Si desea pausar la simulación presione el boton de Stop\n\n" \
               "---Funcionamiento---\nUna vez iniciada la simulación, en el panel izquierdo se adicionaran las sillas " \
               "ingresadas por el usuario y cambiaran su estado automaticamente cuando llega un nuevo cliente" \
               " a la barberia, ademas el fondo se pintará de rojo si la sala de espera está llena.\n" \
               "En el panel derecho se pintará la imagen del barbero con su respectivo estado ya sea durmiendo o " \
               "atentiendo a un cliente.\n"
        messagebox.showinfo(title="Información", message=text)

    def barber_image(self):
        """
        Updates the barber image based on the barber's sleep state.

        """
        while (self.activate):
            barber_is_sleep = self.barberia.get_sleep()
            if barber_is_sleep:
                self.update_barber('source\sources\images\sleep.png')
            else:
                self.update_barber('source\\sources\\images\\barberWakeup.png')

    def chairsImages(self):
        """
        Updates the images of the chairs in the waiting room based on the number of clients.

        """
        while (self.activate):
            x = 0
            y = 0
            sala_espera = self.barberia.get_list()
            if sala_espera == 0:
                for i in range(self.cantidad):
                    self.canvas.configure(bg='white')
                    self.canvas.create_image(x, y, anchor='nw', image=self.silla_imag)
                    x += 80
                    if (x == 400):
                        x = 0
                        y += 80
            elif sala_espera > 0:
                if sala_espera == self.cantidad:
                    for i in range(self.cantidad):
                        self.canvas.configure(bg='#F3B3B3')
                        self.canvas.create_image(x, y, anchor='nw', image=self.esperando_imag)
                        self.canvas.image = self.silla_imag
                        x += 80
                        if (x == 400):
                            x = 0
                            y += 80
            if 0 < sala_espera < self.cantidad:
                libres = self.cantidad - sala_espera
                self.canvas.configure(bg='white')
                for i in range(self.cantidad):
                    if i >= (self.cantidad - libres):
                        self.canvas.create_image(x, y, anchor='nw', image=self.silla_imag)
                        x += 80
                        if (x == 400):
                            x = 0
                            y += 80
                    else:
                        self.canvas.create_image(x, y, anchor='nw', image=self.esperando_imag)
                        x += 80
                    if (x == 400):
                        x = 0
                        y += 80

    def create_components(self):
        """
        Initializes the component attributes used in the GUI.

        """
        self.titleWindow = 'Sleepy Barber'
        self.colorFondo = '#FFFFFF'
        self.colorFuentePrincipal = '#000000'
        self.colorEntry = '#F5F5F5'
        self.mensajeHora = 'Reloj Sistema:'
        self.mensajeTSimulacion = 'Tiempo de simulacion'
        self.mensajeEstadoCpu = 'Estado CPU: '
        self.mensajeColaProcesos = 'Cola de Procesos en:'
        self.fuenteTitulo = ('Mixed', 30)
        self.fuentePrincipal = ('Mixed,20')
        self.mensajeTablaProcesos = 'Cola de procesos: '
        self.list_length_process = [3, 5, 10]

    def create_window(self):
        """
        Creates the main window of the GUI with its configuration and layout.

        """
        self.ventana = tk.Tk()
        self.ventana.geometry("1000x600")
        self.ventana.title(self.titleWindow)
        self.ventana.resizable(0, 0)
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
            
            
    def showGraphicsTimes(self):
        """_summary_
        """
        while self.activate:
            plt.clf() 
            variables = ["Promedio Llegada", "Promedio Atencion"]  # Variable names
            avg_times = [self.barberia.calcular_promedio_llegada(), self.barberia.calcular_promedio_atencion()]  # Average times

            x_pos = np.arange(len(variables))  # x positions for bars

            # Create the bar graph
            plt.bar(x_pos, avg_times, align='center', alpha=0.5)
            plt.xticks(x_pos, variables)  # Set the x-axis tick labels
            plt.yticks(np.arange(min(avg_times) - 1, max(avg_times) + 1, 0.5))
            for time in avg_times:
                plt.axhline(time, color='blue', linestyle='dashed')
            plt.xlabel('Variables')
            plt.ylabel('Average Times')
            plt.title('Average Times for Each Variable')

            plt.pause(0.1) 

    def showGraphics(self):
        """
        Continuously updates and displays the graph showing the number of unattended clients over time.

        """
        tiempos = []  # Lista para almacenar los tiempos de actualización
        clientes_no_atendidos = []  # Lista para almacenar la cantidad de clientes que no fueron atendidos

        while self.activate:
            tiempos.append(time.time())
            clientes_no_atendidos.append(self.barberia.get_clientes_se_fueron())

            # Limitar la cantidad de puntos en la gráfica para una mejor visualización
            if len(tiempos) > 10000:
                tiempos = tiempos[-10000:]
                clientes_no_atendidos = clientes_no_atendidos[-100:]

            # Actualizar los datos de la línea de la gráfica
            self.linea_grafica.set_data(tiempos, clientes_no_atendidos)

            min_y = 0 
            max_y = max(clientes_no_atendidos) + 1  # Límite superior del eje y
            self.ax.set_xlim(min(tiempos) - 0.1, max(tiempos) + 0.1)
            self.ax.set_ylim(min_y, max_y)

            # Pausa para permitir la interactividad de la ventana de la gráfica
            plt.pause(0.5)   



    def add_components(self):
        """
        Adds and configures the GUI components to the main window.

        """
        self.labelTitulo1 = tk.Label(self.ventana, text=self.titleWindow, bg=self.colorFondo,
                                     fg=self.colorFuentePrincipal, font=self.fuenteTitulo)
        self.labelTitulo1.grid(row=0, column=1, columnspan=5)

    # Separador
        self.separador = ttk.Separator(self.ventana, orient='horizontal')
        self.separador.grid(row=0, column=0, sticky='SWE', columnspan=14)
        self.separador2 = ttk.Separator(self.ventana, orient='vertical')
        self.separador2.grid(row=1, column=2, sticky='NS', rowspan=5)
        self.separador3 = ttk.Separator(self.ventana, orient='horizontal')
        self.separador3.grid(row=5, column=0, sticky='SWE', columnspan=14)

        # Crear el botón para abrir la gráfica
        self.btn_grafica = tk.Button(self.ventana, text="Estadisticas", command=self.showGraphics)
        self.btn_grafica.grid(row=7, column=6, sticky='WE')
        self.btn_grafica = tk.Button(self.ventana, text="Tiempos", command=self.showGraphicsTimes)
        self.btn_grafica.grid(row=7, column=7, sticky='WE') 
        # Crear la figura y los ejes de la gráfica
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.linea_grafica, = self.ax.plot([], [])
        self.ax.set_xlabel('Tiempo')
        self.ax.set_ylabel('Clientes que se fueron')
        self.ax.set_title('Cantidad de clientes no atendidos a lo largo del tiempo')
        self.ax.grid(True)

        # numero de sillas
        self.labelEntrySimulacion = tk.Label(self.ventana, text="Numero de sillas: ", border=0, bg=self.colorFondo,
                                             fg=self.colorFuentePrincipal, font=('Mixed', 15))
        self.labelEntrySimulacion.grid(row=7, column=0, sticky='E', columnspan=2)
        self.numeroSillas = tk.Entry(self.ventana, fg=self.colorFuentePrincipal, font=('Mixed', 15))
        self.numeroSillas.grid(row=7, column=2, sticky='E')
        self.imageButtonSimulacion = tk.PhotoImage(file='source\sources\images\play.png')
        self.imageButtonStopSimulacion = tk.PhotoImage(file='source\sources\images\stop.png')
        self.imageButtonInfoSimulacion = tk.PhotoImage(file='source\sources\images\info.png')
        self.bottomStarSimulacion = tk.Button(self.ventana, image=self.imageButtonSimulacion, bd=0, bg=self.colorFondo,
                                              command=self.startSimulation)
        self.bottomStarSimulacion.grid(row=7, column=3, sticky='WE')
        self.bottomStopSimulacion = tk.Button(self.ventana, image=self.imageButtonStopSimulacion, bd=0,
                                              bg=self.colorFondo, command=self.stopSimulation)
        self.bottomStopSimulacion.grid(row=7, column=4, sticky='WE')
        self.bottomInfoSimulacion = tk.Button(self.ventana, image=self.imageButtonInfoSimulacion, bd=0,
                                              bg=self.colorFondo, command=self.showInfo)
        self.bottomInfoSimulacion.grid(row=7, column=5, sticky='WE')

    def create_images(self):
        """
        Loads and creates image objects for the GUI.

        """
        self.imagen_silla = Image.open('source\sources\images\silla.png')
        self.imagen_silla = self.imagen_silla.resize((80, 80))
        self.silla_imag = ImageTk.PhotoImage(self.imagen_silla)
        self.imagen_esperando = Image.open('source\sources\images\esperandojpg.png')
        self.imagen_esperando = self.imagen_esperando.resize((80, 80))
        self.esperando_imag = ImageTk.PhotoImage(self.imagen_esperando)
        self.canvas = Canvas(self.ventana, width=540, height=180)
        self.canvas.grid(row=2, column=0, sticky='E', columnspan=2)
        self.canvas.config(bg='white')
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def create_logs(self):
        """
        Creates a text area to display logs.

        """
        scroll = tk.Scrollbar(self.ventana, orient='vertical')

        self.logs = tk.Text(self.ventana, width=60, height=8, background="white", foreground="Black",
                            yscrollcommand=scroll.set, font=("Helvetica", 12, "bold"))
        self.logs.config(state='disabled')
        self.logs.grid(row=3, column=0, sticky='E', columnspan=2)
        aux_text = " "
        try:
            while self.activate:
                if aux_text != str(self.barberia.get_logs()):
                    self.logs.config(state='normal')
                    self.logs.delete(1.0, tk.END)
                    for i in range(len(self.barberia.get_logs())):
                        self.logs.insert(tk.END, str(self.barberia.get_logs()[i]))
                        self.logs.focus_set()
                        self.logs.see("end")
                    self.logs.config(state='disabled')
                scroll.config(command=self.logs.yview)
                aux_text = str(self.barberia.get_logs())
                time.sleep(0.7)
        except AttributeError:
            print()

    def update_barber(self, path):
        """
        Updates the image of the barber in the GUI.

        Args:
            path (str): The file path of the new image.

        """
        imagen = Image.open(path)
        imagen = imagen.resize((200, 300))
        photo = ImageTk.PhotoImage(imagen)  # Convertir a PhotoImage
        self.sleepBarber.configure(image=photo)
        self.sleepBarber.image = photo  # Actualizar referencia

    # Barbero
    # Cargar la imagen
    def barber_img(self, path):
        """
        Creates and displays the initial image of the barber in the GUI.

        Args:
            path (str): The file path of the image.

        """
        imagen = Image.open(path)
        imagen = imagen.resize((200, 300))
        self.sleepBarberImage = ImageTk.PhotoImage(imagen)
        self.sleepBarber = tk.Label(self.ventana, image=self.sleepBarberImage, bg="white")
        self.sleepBarber.config(bg='white')
        self.sleepBarber.grid(row=2, column=2, sticky='E', columnspan=6)

    def update_gui(self):
        """
        Updates the GUI components periodically.
        """
        self.crear_imagenes()
        self.ventana.after(500, self.update_gui)


# Ejecutar el bucle principal de la aplicación
main = Main()
