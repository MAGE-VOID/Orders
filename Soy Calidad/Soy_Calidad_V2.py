import tkinter as tk
from tkinter import ttk, messagebox

# --- Diccionarios iniciales ---
Productos = {1: 'Pantalones', 2: 'Camisas', 3: 'Corbatas', 4: 'Casacas'}
Precios   = {1: 200.00,      2: 120.00,    3: 50.00,     4: 350.00}
Stock     = {1: 50,          2: 45,        3: 30,        4: 15}

# --- Función para refrescar la lista de productos en el Listbox ---
def refresh_list():
    listbox.delete(0, tk.END)
    # Mostramos los productos en orden de código (key)
    for codigo in sorted(Productos.keys()):
        texto = f"Código: {codigo} | {Productos[codigo]} | Precio: {Precios[codigo]} | Stock: {Stock[codigo]}"
        listbox.insert(tk.END, texto)

# --- Funciones para las operaciones CRUD ---

def agregar_producto():
    """Ventana para agregar un producto (código, nombre, precio, stock)."""
    ventana_agregar = tk.Toplevel(root)
    ventana_agregar.title("Agregar producto")
    ventana_agregar.geometry("300x200")

    # Aplicamos un padding interno a la ventana
    ventana_agregar.config(padx=10, pady=10)

    # Creamos labels y entries con ttk para un mejor estilo
    ttk.Label(ventana_agregar, text="Código:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
    ttk.Label(ventana_agregar, text="Nombre:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
    ttk.Label(ventana_agregar, text="Precio:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
    ttk.Label(ventana_agregar, text="Stock:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)

    entry_codigo = ttk.Entry(ventana_agregar)
    entry_nombre = ttk.Entry(ventana_agregar)
    entry_precio = ttk.Entry(ventana_agregar)
    entry_stock  = ttk.Entry(ventana_agregar)

    entry_codigo.grid(row=0, column=1, padx=5, pady=5)
    entry_nombre.grid(row=1, column=1, padx=5, pady=5)
    entry_precio.grid(row=2, column=1, padx=5, pady=5)
    entry_stock.grid(row=3, column=1, padx=5, pady=5)

    def confirmar_agregar():
        """Función interna para validar e insertar el nuevo producto."""
        try:
            nuevo_codigo = int(entry_codigo.get())
            if nuevo_codigo in Productos:
                messagebox.showerror("Error", f"El código {nuevo_codigo} ya existe.")
                return
            
            nombre = entry_nombre.get().strip()
            precio = float(entry_precio.get())
            stock  = int(entry_stock.get())

            # Insertamos en los diccionarios
            Productos[nuevo_codigo] = nombre
            Precios[nuevo_codigo]   = precio
            Stock[nuevo_codigo]     = stock

            messagebox.showinfo("Éxito", f"Producto '{nombre}' agregado correctamente.")
            ventana_agregar.destroy()
            refresh_list()
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese datos válidos.")

    btn_confirmar = ttk.Button(ventana_agregar, text="Agregar", command=confirmar_agregar)
    btn_confirmar.grid(row=4, column=0, columnspan=2, pady=10)

def eliminar_producto():
    """Ventana para eliminar un producto por su código."""
    ventana_eliminar = tk.Toplevel(root)
    ventana_eliminar.title("Eliminar producto")
    ventana_eliminar.geometry("300x120")
    ventana_eliminar.config(padx=10, pady=10)

    ttk.Label(ventana_eliminar, text="Código a eliminar:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
    entry_codigo = ttk.Entry(ventana_eliminar)
    entry_codigo.grid(row=0, column=1, padx=5, pady=5)

    def confirmar_eliminar():
        """Función interna para validar y eliminar el producto."""
        try:
            codigo_eliminar = int(entry_codigo.get())
            if codigo_eliminar in Productos:
                nombre_eliminado = Productos.pop(codigo_eliminar)
                Precios.pop(codigo_eliminar)
                Stock.pop(codigo_eliminar)
                messagebox.showinfo("Éxito", f"Producto '{nombre_eliminado}' eliminado correctamente.")
                ventana_eliminar.destroy()
                refresh_list()
            else:
                messagebox.showerror("Error", "El código ingresado no existe.")
        except ValueError:
            messagebox.showerror("Error", "Ingrese un código válido.")

    btn_confirmar = ttk.Button(ventana_eliminar, text="Eliminar", command=confirmar_eliminar)
    btn_confirmar.grid(row=1, column=0, columnspan=2, pady=10)

def actualizar_producto():
    """Ventana para actualizar un producto (código, nuevo nombre, precio, stock)."""
    ventana_actualizar = tk.Toplevel(root)
    ventana_actualizar.title("Actualizar producto")
    ventana_actualizar.geometry("300x200")
    ventana_actualizar.config(padx=10, pady=10)

    ttk.Label(ventana_actualizar, text="Código a actualizar:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
    entry_codigo = ttk.Entry(ventana_actualizar)
    entry_codigo.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(ventana_actualizar, text="Nuevo nombre (opcional):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
    ttk.Label(ventana_actualizar, text="Nuevo precio (opcional):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
    ttk.Label(ventana_actualizar, text="Nuevo stock (opcional):").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)

    entry_nombre = ttk.Entry(ventana_actualizar)
    entry_precio = ttk.Entry(ventana_actualizar)
    entry_stock  = ttk.Entry(ventana_actualizar)

    entry_nombre.grid(row=1, column=1, padx=5, pady=5)
    entry_precio.grid(row=2, column=1, padx=5, pady=5)
    entry_stock.grid(row=3, column=1, padx=5, pady=5)

    def confirmar_actualizar():
        """Función interna para validar y actualizar el producto."""
        try:
            codigo_actualizar = int(entry_codigo.get())
            if codigo_actualizar in Productos:
                # Obtenemos los valores ingresados
                nuevo_nombre = entry_nombre.get().strip()
                nuevo_precio = entry_precio.get().strip()
                nuevo_stock  = entry_stock.get().strip()

                # Si el usuario deja el campo en blanco, conservamos el valor anterior
                if nuevo_nombre:
                    Productos[codigo_actualizar] = nuevo_nombre
                if nuevo_precio:
                    Precios[codigo_actualizar]   = float(nuevo_precio)
                if nuevo_stock:
                    Stock[codigo_actualizar]     = int(nuevo_stock)

                messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
                ventana_actualizar.destroy()
                refresh_list()
            else:
                messagebox.showerror("Error", "El código ingresado no existe.")
        except ValueError:
            messagebox.showerror("Error", "Ingrese datos válidos.")

    btn_confirmar = ttk.Button(ventana_actualizar, text="Actualizar", command=confirmar_actualizar)
    btn_confirmar.grid(row=4, column=0, columnspan=2, pady=10)

# --- Configuración de la ventana principal ---
root = tk.Tk()
root.title("Gestión de Productos")
root.geometry("600x400")
root.resizable(False, False)  # Evita que la ventana sea redimensionable

# Estilo con ttk
style = ttk.Style()
style.theme_use("clam")  # Puedes probar con: "default", "clam", "alt", "classic", etc.

# Configuramos algunos estilos (opcional)
style.configure("TLabel", font=("Arial", 11))
style.configure("TButton", font=("Arial", 10, "bold"))
style.configure("Header.TLabel", font=("Arial", 14, "bold"), foreground="#333")

# Frame principal
main_frame = ttk.Frame(root, padding="10 10 10 10")
main_frame.pack(fill=tk.BOTH, expand=True)

# Título principal
lbl_titulo = ttk.Label(main_frame, text="Gestión de Productos", style="Header.TLabel")
lbl_titulo.pack(pady=5)

# Frame para la lista de productos
frame_listbox = ttk.Labelframe(main_frame, text="Lista de Productos", padding="10 10 10 10")
frame_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# Listbox para mostrar los productos
listbox = tk.Listbox(frame_listbox, width=70, height=10)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Barra de scroll para el Listbox
scrollbar = ttk.Scrollbar(frame_listbox, orient=tk.VERTICAL, command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.config(yscrollcommand=scrollbar.set)

# Frame para los botones
frame_botones = ttk.Frame(main_frame)
frame_botones.pack(pady=5)

btn_agregar = ttk.Button(frame_botones, text="Agregar", width=12, command=agregar_producto)
btn_eliminar = ttk.Button(frame_botones, text="Eliminar", width=12, command=eliminar_producto)
btn_actualizar = ttk.Button(frame_botones, text="Actualizar", width=12, command=actualizar_producto)
btn_salir = ttk.Button(frame_botones, text="Salir", width=12, command=root.destroy)

btn_agregar.grid(row=0, column=0, padx=5, pady=5)
btn_eliminar.grid(row=0, column=1, padx=5, pady=5)
btn_actualizar.grid(row=0, column=2, padx=5, pady=5)
btn_salir.grid(row=0, column=3, padx=5, pady=5)

# Inicializar la lista con los datos actuales
refresh_list()

# Iniciar el bucle principal de la aplicación
root.mainloop()
