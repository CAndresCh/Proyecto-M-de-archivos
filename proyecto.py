import json
import os
import shutil
import customtkinter as ctk
from tkinter import colorchooser, filedialog, messagebox

ARCHIVO_CONFIG = 'config.json'
ARCHIVO_RESPALDO = 'config.bak'
ARCHIVO_TEMPORAL = 'config.tmp'

CONFIG_POR_DEFECTO = {
    "nombre_usuario": "Usuario",
    "tema": "Dark",
    "idioma": "es",
    "tamano_fuente": 14,
    "color_menu": "#1f538d",
    "color_letra": "#ffffff",
    "foto_perfil": ""
}

def cargar_configuracion():
    config_actual = CONFIG_POR_DEFECTO.copy()
    if not os.path.exists(ARCHIVO_CONFIG):
        return config_actual
    try:
        with open(ARCHIVO_CONFIG, 'r', encoding='utf-8') as archivo:
            datos_leidos = json.load(archivo)
            config_actual.update(datos_leidos)
            return config_actual
    except json.JSONDecodeError:
        messagebox.showwarning("Advertencia", "El archivo de configuración está corrupto. Se usarán los ajustes por defecto.")
        return config_actual
    except PermissionError:
        messagebox.showwarning("Advertencia", "Sin permisos de lectura en la configuración. Se usarán los ajustes por defecto.")
        return config_actual

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

class Aplicacion(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.datos_config = cargar_configuracion()
        
        ctk.set_appearance_mode(self.datos_config.get("tema", "Dark"))
        ctk.set_default_color_theme("blue")
        
        self.title("Gestión de Configuración - CustomTkinter")
        self.geometry("800x600")
        
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda event: self.attributes("-fullscreen", False)) 
        
        self.crear_menu_superior()
        self.crear_interfaz_principal()

    def crear_menu_superior(self):
        color_fondo = self.datos_config.get("color_menu", "#1f538d")
        
        barra_frame = ctk.CTkFrame(self, height=45, corner_radius=0, fg_color=color_fondo)
        barra_frame.pack(side="top", fill="x")
        
        self.menu_archivo = ctk.CTkOptionMenu(barra_frame, values=["Restaurar Backup (.bak)", "Eliminar Configuración"], command=self.manejar_menu_archivo, width=120, fg_color=("gray75", "gray25"), text_color=("black", "white"), button_color=("gray70", "gray30"), button_hover_color=("gray60", "gray40"))
        self.menu_archivo.set("📁 Archivo")
        self.menu_archivo.pack(side="left", padx=5, pady=6)
        
        self.menu_edicion = ctk.CTkOptionMenu(barra_frame, values=["Restablecer Valores", "Limpiar Foto de Perfil"], command=self.manejar_menu_edicion, width=120, fg_color=("gray75", "gray25"), text_color=("black", "white"), button_color=("gray70", "gray30"), button_hover_color=("gray60", "gray40"))
        self.menu_edicion.set("✏️ Edición")
        self.menu_edicion.pack(side="left", padx=5, pady=6)
        
        ctk.CTkButton(barra_frame, text="👁️ Ver JSON", width=90, fg_color="transparent", text_color=("black", "white"), hover_color=("gray70", "gray30"), command=self.ver_configuracion).pack(side="left", padx=5, pady=6)
        
        ctk.CTkButton(barra_frame, text="❌ Salir", width=80, fg_color="#c93434", text_color="white", hover_color="#992626", command=self.destroy).pack(side="right", padx=(5, 10), pady=6)
        
        ctk.CTkButton(barra_frame, text="⚙️ Settings", width=90, fg_color="#1f538d", text_color="white", hover_color="#14375e", command=self.abrir_configuracion).pack(side="right", padx=5, pady=6)

    def manejar_menu_archivo(self, eleccion):
        if eleccion == "Restaurar Backup (.bak)":
            if os.path.exists(ARCHIVO_RESPALDO):
                shutil.copy(ARCHIVO_RESPALDO, ARCHIVO_CONFIG)
                messagebox.showinfo("Éxito", "Copia de seguridad restaurada correctamente. Se reiniciará la app.")
                self.reiniciar_app()
                return
            else:
                messagebox.showwarning("Error", "No se encontró el archivo config.bak para restaurar.")
        
        elif eleccion == "Eliminar Configuración":
            confirmacion = messagebox.askyesno("Confirmar", "¿Seguro que deseas eliminar el archivo JSON? Perderás tus ajustes.")
            if confirmacion and os.path.exists(ARCHIVO_CONFIG):
                os.remove(ARCHIVO_CONFIG)
                messagebox.showinfo("Éxito", "Archivo eliminado. Se reiniciará la app con valores por defecto.")
                self.reiniciar_app()
                return
                
        self.menu_archivo.set("📁 Archivo")

    def manejar_menu_edicion(self, eleccion):
        if eleccion == "Restablecer Valores":
            if guardar_configuracion(CONFIG_POR_DEFECTO):
                messagebox.showinfo("Éxito", "Valores de fábrica restablecidos. Se reiniciará la app.")
                self.reiniciar_app()
                return
                
        elif eleccion == "Limpiar Foto de Perfil":
            self.datos_config["foto_perfil"] = ""
            if guardar_configuracion(self.datos_config):
                messagebox.showinfo("Éxito", "Foto de perfil eliminada. Se reiniciará la app.")
                self.reiniciar_app()
                return
                
        self.menu_edicion.set("✏️ Edición")

    def reiniciar_app(self):
        self.destroy()
        Aplicacion().mainloop()

    def crear_interfaz_principal(self):
        card = ctk.CTkFrame(self, corner_radius=15, fg_color=("white", "gray20"), width=550, height=320)
        card.place(relx=0.5, rely=0.5, anchor="center")
        
        tamano_fuente = self.datos_config.get("tamano_fuente", 14)
        nombre = self.datos_config.get("nombre_usuario", "Usuario")
        ruta_foto = self.datos_config.get("foto_perfil", "")
        color_texto = self.datos_config.get("color_letra", "#ffffff")
        
        ctk.CTkLabel(card, text=f"¡Bienvenido, {nombre}!", font=ctk.CTkFont(family="Helvetica", size=tamano_fuente + 6, weight="bold"), text_color=color_texto).pack(pady=(35, 10))
        ctk.CTkLabel(card, text="Aplicación de Escritorio con Gestión de Configuración Segura", font=ctk.CTkFont(size=12), text_color="gray").pack(pady=(0, 20))
        
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(fill="x", padx=30, pady=10)
        
        ctk.CTkLabel(info_frame, text=f"🌐 Idioma actual: {self.datos_config.get('idioma', 'es')}", font=ctk.CTkFont(size=13)).pack(anchor="w", pady=2)
        
        foto_texto = f"🖼️ Foto: {os.path.basename(ruta_foto)}" if ruta_foto else "🖼️ Sin foto de perfil seleccionada"
        ctk.CTkLabel(info_frame, text=foto_texto, font=ctk.CTkFont(size=12), text_color=("gray40", "gray60")).pack(anchor="w", pady=2)

        ctk.CTkButton(card, text="Abrir Panel de Settings", command=self.abrir_configuracion, fg_color="#2b825c", hover_color="#1f5e42", font=ctk.CTkFont(weight="bold")).pack(pady=20)

    def ver_configuracion(self):
        info = "Configuración Actual Almacenada:\n\n"
        for clave, valor in self.datos_config.items():
            info += f"• {clave}: {valor}\n"
        messagebox.showinfo("Ver Configuración (JSON)", info)

    def abrir_configuracion(self):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Settings - Configuración de Usuario")
        ventana.geometry("450x520")
        ventana.grab_set() 
        
        tabview = ctk.CTkTabview(ventana, width=410, height=430)
        tabview.pack(padx=20, pady=10)
        
        tab_general = tabview.add("General")
        tab_apariencia = tabview.add("Apariencia")
        
        var_nombre = ctk.StringVar(value=self.datos_config["nombre_usuario"])
        var_tema = ctk.StringVar(value=self.datos_config["tema"])
        var_idioma = ctk.StringVar(value=self.datos_config["idioma"])
        var_fuente = ctk.StringVar(value=str(self.datos_config["tamano_fuente"]))
        
        ctk.CTkLabel(tab_general, text="Nombre de Usuario:", anchor="w").pack(fill="x", padx=15, pady=(15, 5))
        ctk.CTkEntry(tab_general, textvariable=var_nombre).pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(tab_general, text="Idioma:", anchor="w").pack(fill="x", padx=15, pady=(15, 5))
        ctk.CTkComboBox(tab_general, values=["es", "es-ES", "en", "en-US"], variable=var_idioma, state="readonly").pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(tab_general, text="Foto de Perfil:", anchor="w").pack(fill="x", padx=15, pady=(15, 5))
        ctk.CTkButton(tab_general, text="Seleccionar Imagen...", command=self.elegir_foto, fg_color="gray50", hover_color="gray40").pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(tab_apariencia, text="Tema de Interfaz (Modo):", anchor="w").pack(fill="x", padx=15, pady=(15, 5))
        ctk.CTkComboBox(tab_apariencia, values=["Dark", "Light"], variable=var_tema, state="readonly").pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(tab_apariencia, text="Tamaño de Fuente (Entero):", anchor="w").pack(fill="x", padx=15, pady=(15, 5))
        ctk.CTkEntry(tab_apariencia, textvariable=var_fuente).pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(tab_apariencia, text="Colores Personalizados:", anchor="w").pack(fill="x", padx=15, pady=(15, 5))
        frame_colores = ctk.CTkFrame(tab_apariencia, fg_color="transparent")
        frame_colores.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkButton(frame_colores, text="Color Menú", command=lambda: self.elegir_color("color_menu"), fg_color="#3b71ca", hover_color="#28519e").pack(side="left", expand=True, padx=(0, 5))
        ctk.CTkButton(frame_colores, text="Color Letra", command=lambda: self.elegir_color("color_letra"), fg_color="#3b71ca", hover_color="#28519e").pack(side="right", expand=True, padx=(5, 0))

        def guardar_cambios():
            try:
                tamano = int(var_fuente.get())
            except ValueError:
                messagebox.showerror("Error de validación", "El tamaño de fuente debe ser un número entero válido.")
                return

            self.datos_config["nombre_usuario"] = var_nombre.get()
            self.datos_config["tema"] = var_tema.get()
            self.datos_config["idioma"] = var_idioma.get()
            self.datos_config["tamano_fuente"] = tamano
            
            if guardar_configuracion(self.datos_config):
                messagebox.showinfo("Éxito", "Configuración guardada de forma segura (.tmp / .bak). Reiniciando app...")
                self.reiniciar_app()

        ctk.CTkButton(ventana, text="💾 Guardar Configuración", command=guardar_cambios, fg_color="#2b825c", hover_color="#1f5e42", height=38, font=ctk.CTkFont(weight="bold")).pack(fill="x", padx=35, pady=10)

    def elegir_color(self, clave):
        codigo_color = colorchooser.askcolor(title="Seleccionar Color")[1]
        if codigo_color:
            self.datos_config[clave] = codigo_color
            messagebox.showinfo("Color Seleccionado", f"Color guardado: {codigo_color}")

    def elegir_foto(self):
        archivo_foto = filedialog.askopenfilename(title="Seleccionar foto de perfil", filetypes=[("Archivos de imagen", "*.png *.jpg *.jpeg")])
        if archivo_foto:
            self.datos_config["foto_perfil"] = archivo_foto
            messagebox.showinfo("Foto Seleccionada", "Ruta de foto actualizada.")

app = Aplicacion()
app.mainloop()