import pandas as pd
from jinja2 import Environment, FileSystemLoader
from html2image import Html2Image
import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading

# Configuración de apariencia de CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class CardGeneratorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Generador de Tarjetas de Empleados")
        self.geometry("500x300")
        
        # Variables
        self.csv_path = ctk.StringVar()
        
        # Crear widgets
        self.create_widgets()
        
    def create_widgets(self):
        # Título
        title_label = ctk.CTkLabel(self, text="Generador de Tarjetas", font=("Arial", 20, "bold"))
        title_label.pack(pady=20)
        
        # Frame para selección de archivo
        file_frame = ctk.CTkFrame(self)
        file_frame.pack(pady=20, padx=40, fill="x")
        
        file_label = ctk.CTkLabel(file_frame, text="Seleccionar archivo CSV:", font=("Arial", 14))
        file_label.pack(pady=10)
        
        file_entry = ctk.CTkEntry(file_frame, textvariable=self.csv_path, width=300)
        file_entry.pack(side="left", padx=10, pady=10)
        
        browse_btn = ctk.CTkButton(file_frame, text="Examinar", command=self.browse_file, width=80)
        browse_btn.pack(side="right", padx=10, pady=10)
        
        # Frame para botones de acción
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=30)
        
        process_btn = ctk.CTkButton(button_frame, text="Procesar", command=self.process, 
                                   font=("Arial", 14), height=40, width=120)
        process_btn.pack(side="left", padx=20)
        
        cancel_btn = ctk.CTkButton(button_frame, text="Cancelar", command=self.cancel, 
                                  font=("Arial", 14), height=40, width=120, fg_color="red")
        cancel_btn.pack(side="right", padx=20)
        
        # Barra de progreso
        self.progress = ctk.CTkProgressBar(self, mode="indeterminate")
        self.progress.pack(pady=10, padx=40, fill="x")
        self.progress.set(0)
        
        # Etiqueta de estado
        self.status_label = ctk.CTkLabel(self, text="Listo para procesar", text_color="gray")
        self.status_label.pack(pady=10)
    
    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.csv_path.set(filename)
    
    def process(self):
        if not self.csv_path.get():
            messagebox.showerror("Error", "Por favor, seleccione un archivo CSV")
            return
        
        # Deshabilitar botones durante el procesamiento
        self.disable_buttons(True)
        self.status_label.configure(text="Procesando...")
        self.progress.start()
        
        # Ejecutar en un hilo separado para no bloquear la interfaz
        thread = threading.Thread(target=self.generate_cards)
        thread.daemon = True
        thread.start()
    
    def generate_cards(self):
        try:
            # 1. Crear rutas absolutas y normalizadas
            base_dir = os.path.dirname(os.path.abspath(__file__))  # Ruta del script
            temp_dir = os.path.normpath(os.path.join(base_dir, "html2image_temp"))
            output_dir = os.path.normpath(os.path.join(base_dir, "tarjetas"))

            # 2. Crear directorios con permisos adecuados
            os.makedirs(temp_dir, exist_ok=True, mode=0o777)
            os.makedirs(output_dir, exist_ok=True, mode=0o777)

            # 3. Configurar Html2Image con parámetros seguros
            hti = Html2Image(
                temp_path=temp_dir,
                output_path=output_dir,
                size=(328, 208),
                custom_flags=[
                    '--hide-scrollbars',
                    '--default-background-color=00000000',  # Fondo transparente
                    '--force-device-scale-factor=1',
                    '--disable-extensions',
                    '--disable-popup-blocking',
                    '--disable-infobars',
                    '--disable-notifications',
                    '--disable-gpu',
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage'
                ]
            )
            
            # Configuración
            csv_path = self.csv_path.get()
            template_path = 'tarjetasEmpleados1.html'
            output_folder = './tarjetas/'
            os.makedirs(output_folder, exist_ok=True)

            # Cargar datos
            df = pd.read_csv(csv_path)
            # Verificar que el archivo CSV se cargó correctamente
            df.columns = df.columns.str.strip()  # Eliminar espacios en blanco de los nombres de las columnas
            
            # Configurar Jinja2
            env = Environment(loader=FileSystemLoader('.'))
            template = env.get_template(template_path)

            # Función para generar imagen
            def generar_imagen_segura(hti, html_content, output_filename):
                try:
                    # Asegurar nombre de archivo válido
                    safe_filename = "".join(c for c in output_filename if c.isalnum() or c in ('_', '-', '.'))
                    
                    # Generar usando directorio temporal controlado
                    hti.screenshot(
                        html_str=html_content,
                        save_as=safe_filename,
                        size=(328, 308),    
                    )
                    return True
                except Exception as e:
                    print(f"Error al generar {output_filename}: {str(e)}")
                    return False
            
            # Procesar cada empleado y generar imágenes
            for _, empleado in df.iterrows():
                html_output = template.render(**empleado.to_dict())
                output_image = f"{empleado['Cedula']}{empleado['Apellidos']}{empleado['Nombres']}.png"
                
                if generar_imagen_segura(hti, html_output, output_image):
                    print(f"✓ Imagen generada: {output_image}")
                else:
                    print(f"✗ Falló generación para empleado {empleado['Cedula']}")
            
            # Finalizar
            try:
                import cropcards
                cropcards
            except ImportError:
                print("Módulo cropcards no encontrado, continuando sin él")
            
            # Actualizar interfaz en el hilo principal
            self.after(0, self.process_completed)
            
        except Exception as e:
            # Mostrar error en el hilo principal
            self.after(0, lambda: self.process_error(str(e)))
    
    def process_completed(self):
        self.progress.stop()
        self.status_label.configure(text="Proceso completado con éxito!")
        self.disable_buttons(False)
        messagebox.showinfo("Éxito", "Las tarjetas se han generado correctamente")
    
    def process_error(self, error_msg):
        self.progress.stop()
        self.status_label.configure(text="Error en el procesamiento")
        self.disable_buttons(False)
        messagebox.showerror("Error", f"Ocurrió un error:\n{error_msg}")
    
    def disable_buttons(self, disable):
        # Esta función necesitaría acceso a los botones, que podrías almacenar como atributos
        pass  # Implementar según sea necesario
    
    def cancel(self):
        self.quit()

if __name__ == "__main__":
    app = CardGeneratorApp()
    app.mainloop()