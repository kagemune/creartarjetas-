import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import sys


# if sys.stdout.encoding != 'utf-8':
#     sys.stdout.reconfigure(encoding='utf-8')


class CSVProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Tarjetas de Empleados")
        self.root.geometry("500x300")
        self.root.resizable(False, False)
        
        # Centrar la ventana
        self.center_window(500, 300)
        
        # Variable para almacenar la ruta del CSV
        self.csv_path = tk.StringVar()
        
        # Configurar la interfaz
        self.setup_ui()
    
    def center_window(self, width, height):
        """Centrar la ventana en la pantalla"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_ui(self):
        """Configurar los elementos de la interfaz"""
        # Título
        title_label = tk.Label(
            self.root, 
            text="Generador de Tarjetas de Contratistas",
            font=("Arial", 16, "bold"),
            pady=10
        )
        title_label.pack()
        
        # Frame para selección de archivo
        file_frame = tk.Frame(self.root)
        file_frame.pack(pady=20, padx=20, fill="x")
        
        tk.Label(
            file_frame, 
            text="Archivo CSV:", 
            font=("Arial", 10)
        ).pack(anchor="w")
        
        # Entry y botón para seleccionar archivo
        entry_frame = tk.Frame(file_frame)
        entry_frame.pack(fill="x", pady=5)
        
        tk.Entry(
            entry_frame, 
            textvariable=self.csv_path, 
            font=("Arial", 10),
            state="readonly"
        ).pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        tk.Button(
            entry_frame, 
            text="Examinar", 
            command=self.browse_csv,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold")
        ).pack(side="right")
        
        # Frame para botones de acción
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        # Botón Procesar
        tk.Button(
            button_frame, 
            text="Procesar", 
            command=self.process_csv,
            bg="#2196F3",
            fg="white",
            font=("Arial", 12, "bold"),
            width=10,
            height=2
        ).pack(side="left", padx=10)
        
        # Botón Cancelar
        tk.Button(
            button_frame, 
            text="Cancelar", 
            command=self.root.quit,
            bg="#f44336",
            fg="white",
            font=("Arial", 12, "bold"),
            width=10,
            height=2
        ).pack(side="right", padx=10)
    
    def browse_csv(self):
        """Abrir diálogo para seleccionar archivo CSV"""
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo CSV",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
        )
        
        if file_path:
            self.csv_path.set(file_path)
    
    def process_csv(self):
        """Ejecutar el script original con el CSV seleccionado"""
        if not self.csv_path.get():
            messagebox.showerror("Error", "Por favor, seleccione un archivo CSV")
            return
        
        try:
            # Copiar el archivo CSV seleccionado al directorio actual
            # para que el script original pueda encontrarlo como 'novedades.csv'
            import shutil
            shutil.copy2(self.csv_path.get(), "novedades.csv")
            
            # Mostrar mensaje de progreso
            progress_window = tk.Toplevel(self.root)
            progress_window.title("Procesando")
            progress_window.geometry("300x100")
            progress_window.resizable(False, False)
            progress_window.grab_set()  # Hacer la ventana modal
            
            # Centrar ventana de progreso
            progress_window.update_idletasks()
            x = self.root.winfo_x() + (self.root.winfo_width() - 300) // 2
            y = self.root.winfo_y() + (self.root.winfo_height() - 100) // 2
            progress_window.geometry(f"300x100+{x}+{y}")
            
            tk.Label(
                progress_window, 
                text="Generando tarjetas...\nPor favor espere.",
                font=("Arial", 11),
                pady=20
            ).pack()
            
            progress_window.update()
            
            # Ejecutar el script original
            result = subprocess.run(
                [sys.executable, "cardgenerator contratistas.py"],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            # Cerrar ventana de progreso
            progress_window.destroy()
            
            if result.returncode == 0:
                messagebox.showinfo("Éxito", "Las tarjetas se han generado correctamente.")
            else:
                messagebox.showerror("Error", f"Ocurrió un error al procesar el archivo:\n\n{result.stderr}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado:\n\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVProcessorApp(root)
    root.mainloop()