# Importar las bibliotecas necesarias
import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import csv
import locale

# Establecer la configuración regional para el formato de moneda
locale.setlocale(locale.LC_ALL, 'es_CL.UTF-8')

# Función para agregar un producto
def agregar_producto():
    # Función interna para guardar un nuevo producto en la base de datos
    def guardar_producto():
        # Obtener los valores de los campos de entrada
        fecha = entry_fecha.get()
        producto = entry_producto.get()
        categoria = entry_categoria.get()
        precio = float(entry_precio.get().replace('.', '').replace(',', '.'))
        cantidad = int(entry_cantidad.get())
        total = precio * cantidad
        
        # Conectar a la base de datos y ejecutar la consulta para insertar el producto
        with sqlite3.connect('ventas.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO ventas (fecha, producto, categoria, precio, cantidad, total)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (fecha, producto, categoria, precio, cantidad, total))
            conn.commit()
        
        # Mostrar un mensaje de éxito
        messagebox.showinfo("Éxito", "Producto agregado exitosamente")
        ventana_agregar.destroy()

    # Crear la ventana para agregar un producto
    ventana_agregar = tk.Toplevel(root)
    ventana_agregar.title("Agregar Producto")
    ventana_agregar.geometry("400x300")
    ventana_agregar.configure(bg="#e1e1e1")
    
    # Crear etiquetas y campos de entrada para los datos del producto
    tk.Label(ventana_agregar, text="Fecha (YYYY-MM-DD):", bg="#e1e1e1").pack(pady=5)
    entry_fecha = tk.Entry(ventana_agregar)
    entry_fecha.pack(pady=5)
    
    tk.Label(ventana_agregar, text="Producto:", bg="#e1e1e1").pack(pady=5)
    entry_producto = tk.Entry(ventana_agregar)
    entry_producto.pack(pady=5)
    
    tk.Label(ventana_agregar, text="Categoría:", bg="#e1e1e1").pack(pady=5)
    entry_categoria = tk.Entry(ventana_agregar)
    entry_categoria.pack(pady=5)
    
    tk.Label(ventana_agregar, text="Precio (CLP):", bg="#e1e1e1").pack(pady=5)
    entry_precio = tk.Entry(ventana_agregar)
    entry_precio.pack(pady=5)
    
    tk.Label(ventana_agregar, text="Cantidad:", bg="#e1e1e1").pack(pady=5)
    entry_cantidad = tk.Entry(ventana_agregar)
    entry_cantidad.pack(pady=5)
    
    # Botón para guardar el producto
    tk.Button(ventana_agregar, text="Guardar", command=guardar_producto, bg="#4caf50", fg="white").pack(pady=20)

# Función para actualizar un producto existente
def actualizar_producto():
    # Función interna para guardar los cambios de un producto en la base de datos
    def guardar_cambios(id_producto):
        # Obtener los valores de los campos de entrada
        fecha = entry_fecha.get()
        producto = entry_producto.get()
        categoria = entry_categoria.get()
        precio = float(entry_precio.get().replace('.', '').replace(',', '.'))
        cantidad = int(entry_cantidad.get())
        total = precio * cantidad
        
        # Conectar a la base de datos y ejecutar la consulta para actualizar el producto
        with sqlite3.connect('ventas.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE ventas 
                SET fecha=?, producto=?, categoria=?, precio=?, cantidad=?, total=? 
                WHERE id=?
            ''', (fecha, producto, categoria, precio, cantidad, total, id_producto))
            conn.commit()
        
        # Mostrar un mensaje de éxito
        messagebox.showinfo("Éxito", "Producto actualizado exitosamente")
        ventana_actualizar.destroy()

    # Función interna para seleccionar un producto por su ID
    def seleccionar_producto():
        # Obtener el ID del producto desde el campo de entrada
        id_producto = int(entry_id.get())
        # Conectar a la base de datos y buscar el producto por su ID
        with sqlite3.connect('ventas.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ventas WHERE id=?", (id_producto,))
            producto = cursor.fetchone()
        
        # Si se encuentra el producto, cargar sus datos en los campos de entrada
        if producto:
            entry_fecha.delete(0, tk.END)
            entry_fecha.insert(0, producto[1])
            entry_producto.delete(0, tk.END)
            entry_producto.insert(0, producto[2])
            entry_categoria.delete(0, tk.END)
            entry_categoria.insert(0, producto[3])
            entry_precio.delete(0, tk.END)
            entry_precio.insert(0, locale.format_string('%.2f', producto[4], grouping=True))
            entry_cantidad.delete(0, tk.END)
            entry_cantidad.insert(0, producto[5])
        else:
            messagebox.showerror("Error", "Producto no encontrado")

    # Crear la ventana para actualizar un producto
    ventana_actualizar = tk.Toplevel(root)
    ventana_actualizar.title("Actualizar Producto")
    ventana_actualizar.geometry("400x300")
    ventana_actualizar.configure(bg="#e1e1e1")
    
    # Crear etiquetas y campos de entrada para los datos del producto
    tk.Label(ventana_actualizar, text="ID del Producto:", bg="#e1e1e1").pack(pady=5)
    entry_id = tk.Entry(ventana_actualizar)
    entry_id.pack(pady=5)

    # Botón para seleccionar el producto por su ID
    tk.Button(ventana_actualizar, text="Seleccionar Producto", command=seleccionar_producto, bg="#2196f3", fg="white").pack(pady=10)
    
    tk.Label(ventana_actualizar, text="Fecha (YYYY-MM-DD):", bg="#e1e1e1").pack(pady=5)
    entry_fecha = tk.Entry(ventana_actualizar)
    entry_fecha.pack(pady=5)
    
    tk.Label(ventana_actualizar, text="Producto:", bg="#e1e1e1").pack(pady=5)
    entry_producto = tk.Entry(ventana_actualizar)
    entry_producto.pack(pady=5)
    
    tk.Label(ventana_actualizar, text="Categoría:", bg="#e1e1e1").pack(pady=5)
    entry_categoria = tk.Entry(ventana_actualizar)
    entry_categoria.pack(pady=5)
    
    tk.Label(ventana_actualizar, text="Precio (CLP):", bg="#e1e1e1").pack(pady=5)
    entry_precio = tk.Entry(ventana_actualizar)
    entry_precio.pack(pady=5)
    
    tk.Label(ventana_actualizar, text="Cantidad:", bg="#e1e1e1").pack(pady=5)
    entry_cantidad = tk.Entry(ventana_actualizar)
    entry_cantidad.pack(pady=5)
    
    # Botón para guardar los cambios del producto
    tk.Button(ventana_actualizar, text="Guardar Cambios", command=lambda: guardar_cambios(entry_id.get()), bg="#4caf50", fg="white").pack(pady=20)

# Función para eliminar un producto
def eliminar_producto():
    # Función interna para eliminar un producto de la base de datos
    def borrar_producto():
        # Obtener el ID del producto desde el campo de entrada
        id_producto = entry_id.get()
        # Conectar a la base de datos y ejecutar la consulta para eliminar el producto por su ID
        with sqlite3.connect('ventas.db') as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ventas WHERE id=?", (id_producto,))
            conn.commit()
        
        # Mostrar un mensaje de éxito
        messagebox.showinfo("Éxito", "Producto eliminado exitosamente")
        ventana_eliminar.destroy()

    # Crear la ventana para eliminar un producto
    ventana_eliminar = tk.Toplevel(root)
    ventana_eliminar.title("Eliminar Producto")
    ventana_eliminar.geometry("300x150")
    ventana_eliminar.configure(bg="#e1e1e1")
    
    # Crear etiquetas y campos de entrada para el ID del producto
    tk.Label(ventana_eliminar, text="ID del Producto:", bg="#e1e1e1").pack(pady=5)
    entry_id = tk.Entry(ventana_eliminar)
    entry_id.pack(pady=5)
    
    # Botón para eliminar el producto
    tk.Button(ventana_eliminar, text="Eliminar Producto", command=borrar_producto, bg="#f44336", fg="white").pack(pady=10)

# Función para ver todos los productos en una tabla con formato de planilla de Excel
def ver_productos():
    # Crear la ventana para ver los productos
    ventana_ver = tk.Toplevel(root)
    ventana_ver.title("Ver Productos")
    ventana_ver.geometry("800x600")
    ventana_ver.configure(bg="#f0f0f0")
    
    # Crear una tabla (TreeView) para mostrar los productos
    tree = ttk.Treeview(ventana_ver, columns=("ID", "Fecha", "Producto", "Categoría", "Precio", "Cantidad", "Total"), show="headings")
    tree.pack(pady=20)
    tree.heading("ID", text="ID", anchor=tk.CENTER)
    tree.heading("Fecha", text="Fecha", anchor=tk.CENTER)
    tree.heading("Producto", text="Producto", anchor=tk.CENTER)
    tree.heading("Categoría", text="Categoría", anchor=tk.CENTER)
    tree.heading("Precio", text="Precio (CLP)", anchor=tk.CENTER)
    tree.heading("Cantidad", text="Cantidad", anchor=tk.CENTER)
    tree.heading("Total", text="Total", anchor=tk.CENTER)
    
    # Establecer el estilo de la tabla para que se vea como una planilla de Excel
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
    style.configure("Treeview", font=("Arial", 10))
    style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])  # Eliminar el borde de la tabla
    
    # Obtener los datos de los productos desde la base de datos y mostrarlos en la tabla
    with sqlite3.connect('ventas.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ventas")
        registros = cursor.fetchall()
    
    for i, registro in enumerate(registros, start=1):
        # Formatear el precio como moneda (CLP)
        precio = locale.format_string('%.2f', registro[4], grouping=True)
        # Insertar cada registro en la tabla
        if i % 2 == 0:
            tree.insert("", "end", values=(registro[0], registro[1], registro[2], registro[3], precio, registro[5], registro[6]), tags=("even",))
        else:
            tree.insert("", "end", values=(registro[0], registro[1], registro[2], registro[3], precio, registro[5], registro[6]), tags=("odd",))
    
    # Aplicar el estilo a las filas alternas
    tree.tag_configure("even", background="#f0f0f0")
    tree.tag_configure("odd", background="#e1e1e1")

# Función para exportar los productos a un archivo CSV
def exportar_csv():
    # Obtener todos los productos desde la base de datos
    with sqlite3.connect('ventas.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ventas")
        registros = cursor.fetchall()
    
    # Escribir los productos en un archivo CSV
    with open('ventas.csv', 'w', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        escritor_csv.writerow(['ID', 'Fecha', 'Producto', 'Categoría', 'Precio', 'Cantidad', 'Total'])
        escritor_csv.writerows(registros)
    
    # Mostrar un mensaje de éxito
    messagebox.showinfo("Éxito", "Datos exportados a ventas.csv")

# Crear la ventana principal
root = tk.Tk()
root.title("Panel de Control de Ventas")
root.geometry("800x600")
root.configure(bg="#f0f0f0")

# Diseño del panel principal
frame = tk.Frame(root, bg="#f0f0f0")
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Etiqueta para el título del panel principal
tk.Label(frame, text="Panel de Control de Ventas", font=("Arial", 24), bg="#f0f0f0").grid(row=0, columnspan=4, pady=20)

# Botones para realizar acciones en el panel principal
btn_agregar = tk.Button(frame, text="Agregar Producto", command=agregar_producto, width=20, height=2, bg="#2196f3", fg="white")
btn_agregar.grid(row=1, column=0, padx=10, pady=10)

btn_actualizar = tk.Button(frame, text="Actualizar Producto", command=actualizar_producto, width=20, height=2, bg="#ffc107", fg="black")
btn_actualizar.grid(row=1, column=1, padx=10, pady=10)

btn_eliminar = tk.Button(frame, text="Eliminar Producto", command=eliminar_producto, width=20, height=2, bg="#ff5722", fg="white")
btn_eliminar.grid(row=1, column=2, padx=10, pady=10)

btn_ver = tk.Button(frame, text="Ver Productos", command=ver_productos, width=20, height=2, bg="#4caf50", fg="white")
btn_ver.grid(row=1, column=3, padx=10, pady=10)

btn_exportar = tk.Button(frame, text="Exportar CSV", command=exportar_csv, width=20, height=2, bg="#ff9800", fg="white")
btn_exportar.grid(row=2, column=1, columnspan=2, padx=10, pady=10)

btn_salir = tk.Button(frame, text="Salir", command=root.quit, width=20, height=2, bg="#f44336", fg="white")
btn_salir.grid(row=2, column=3, padx=10, pady=10)

# Ejecutar la aplicación
root.mainloop()
