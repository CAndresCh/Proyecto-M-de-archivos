import json
import os
import shutil
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import colorchooser, filedialog, messagebox

#CONFIGURACIÓN DE ARCHIVOS
ARCHIVO_CONFIG = 'config.json'
ARCHIVO_RESPALDO = 'config.bak'
ARCHIVO_TEMPORAL = 'config.tmp'

CONFIG_POR_DEFECTO = {
    "nombre_usuario": "Usuario",
    "tema": "litera",
    "idioma": "es",
    "tamano_fuente": 12,
    "color_menu": "#ffffff",
    "color_letra": "#000000",
    "foto_perfil": ""
}

def cargar_configuracion():
    if not os.path.exists(ARCHIVO_CONFIG):
        return CONFIG_POR_DEFECTO.copy()
    try:
        with open(ARCHIVO_CONFIG, 'r', encoding='utf-8') as archivo:
            return json.load(archivo)
    except json.JSONDecodeError:
        messagebox.showwarning("Advertencia", "El archivo de configuración está corrupto. Se usarán los ajustes por defecto.")
        return CONFIG_POR_DEFECTO.copy()
    except PermissionError:
        messagebox.showwarning("Advertencia", "Sin permisos de lectura en la configuración. Se usarán los ajustes por defecto.")
        return CONFIG_POR_DEFECTO.copy()

def guardar_configuracion(nuevos_datos):
    try:
        if os.path.exists(ARCHIVO_CONFIG):
            shutil.copy(ARCHIVO_CONFIG, ARCHIVO_RESPALDO)
            
        with open(ARCHIVO_TEMPORAL, 'w', encoding='utf-8') as archivo:
            json.dump(nuevos_datos, archivo, ensure_ascii=False, indent=4)
            
        os.replace(ARCHIVO_TEMPORAL, ARCHIVO_CONFIG)
        return True
    except PermissionError:
        messagebox.showerror("Error", "Falta de permisos para escribir el archivo.")
        return False
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")
        return False

#INTERFAZ
class Aplicacion(tb.Window):
    def __init__(self):
        self.datos_config = cargar_configuracion()
        
        super().__init__(themename=self.datos_config["tema"])
        self.title("Aplicación de Gestión de Configuración")
        self.geometry("600x400")
        
        self.crear_menu()
        
        tamano_fuente = self.datos_config.get("tamano_fuente", 12)
        color_texto = self.datos_config.get("color_letra", "#000000")
        ruta_foto = self.datos_config.get("foto_perfil", "")
        
        self.label_bienvenida = tb.Label(
            self, 
            text=f"Bienvenido, {self.datos_config['nombre_usuario']}", 
            font=("Helvetica", tamano_fuente),
            foreground=color_texto
        )
        self.label_bienvenida.pack(pady=50)

        if ruta_foto:
            tb.Label(self, text=f"Ruta de foto cargada:\n{ruta_foto}", justify="center").pack(pady=10)

    def crear_menu(self):
        color_fondo_menu = self.datos_config.get("color_menu", "#ffffff")
        barra_menu = tb.Menu(self, bg=color_fondo_menu)
        
        menu_archivo = tb.Menu(barra_menu, tearoff=0)
        menu_archivo.add_command(label="Subopción Simulada")
        barra_menu.add_cascade(label="Archivo", menu=menu_archivo)
        
        menu_edicion = tb.Menu(barra_menu, tearoff=0)
        menu_edicion.add_command(label="Simulado")
        barra_menu.add_cascade(label="Edición", menu=menu_edicion)
        
        menu_ver = tb.Menu(barra_menu, tearoff=0)
        menu_ver.add_command(label="Ver Configuración Actual", command=self.ver_configuracion)
        barra_menu.add_cascade(label="Ver", menu=menu_ver)
        
        menu_configuracion = tb.Menu(barra_menu, tearoff=0)
        menu_configuracion.add_command(label="Abrir Settings", command=self.abrir_configuracion)
        barra_menu.add_cascade(label="Settings", menu=menu_configuracion)
        
        self.config(menu=barra_menu)

    def abrir_configuracion(self):
        ventana = tb.Toplevel(self)
        ventana.title("Configuración de Usuario")
        ventana.geometry("400x500")
        
        var_nombre = tb.StringVar(value=self.datos_config["nombre_usuario"])
        var_tema = tb.StringVar(value=self.datos_config["tema"])
        var_idioma = tb.StringVar(value=self.datos_config["idioma"])
        var_fuente = tb.IntVar(value=self.datos_config["tamano_fuente"])
        
        # Formulario
        tb.Label(ventana, text="Nombre de Usuario:").pack(pady=5)
        tb.Entry(ventana, textvariable=var_nombre).pack()
        
        tb.Label(ventana, text="Tema (Claro/Oscuro):").pack(pady=5)
        temas = ["litera", "darkly"] 
        tb.Combobox(ventana, textvariable=var_tema, values=temas, state="readonly").pack()
        
        tb.Label(ventana, text="Idioma:").pack(pady=5)
        idiomas = ["es", "es-ES", "en", "en-US"]
        tb.Combobox(ventana, textvariable=var_idioma, values=idiomas, state="readonly").pack()
        
        tb.Label(ventana, text="Tamaño de Fuente:").pack(pady=5)
        tb.Entry(ventana, textvariable=var_fuente).pack()
        
        tb.Button(ventana, text="Elegir Color Menú", bootstyle=INFO, command=lambda: self.elegir_color("color_menu")).pack(pady=5)
        tb.Button(ventana, text="Elegir Color de Letra", bootstyle=INFO, command=lambda: self.elegir_color("color_letra")).pack(pady=5)
        tb.Button(ventana, text="Elegir Foto Perfil", bootstyle=INFO, command=self.elegir_foto).pack(pady=5)
        
        def guardar_cambios():
            try:
                tamano = var_fuente.get()
            except tb.tk.TclError:
                messagebox.showerror("Error de validación", "El tamaño de fuente debe ser un número entero válido.")
                return # Detiene el guardado si hay error

            self.datos_config["nombre_usuario"] = var_nombre.get()
            self.datos_config["tema"] = var_tema.get()
            self.datos_config["idioma"] = var_idioma.get()
            self.datos_config["tamano_fuente"] = tamano
                
            if guardar_configuracion(self.datos_config):
                messagebox.showinfo("Éxito", "Configuración guardada. Reinicie para aplicar cambios.")
                ventana.destroy()

    def ver_configuracion(self):
        # Muestra los datos actuales en una ventana de mensaje
        info = "Configuración Actual:\n\n"
        for clave, valor in self.datos_config.items():
            info += f"- {clave}: {valor}\n"
        messagebox.showinfo("Ver Configuración", info)

    def elegir_color(self, clave):
        codigo_color = colorchooser.askcolor(title="Elige un color")[1]
        if codigo_color:
            self.datos_config[clave] = codigo_color
            
    def elegir_foto(self):
        archivo_foto = filedialog.askopenfilename(title="Seleccionar foto", filetypes=[("Archivos de imagen", "*.png *.jpg *.jpeg")])
        if archivo_foto:
            self.datos_config["foto_perfil"] = archivo_foto

aplicacion = Aplicacion()
aplicacion.mainloop()