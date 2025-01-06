# Diccionarios iniciales
Productos = {1: 'Pantalones', 2: 'Camisas', 3: 'Corbatas', 4: 'Casacas'}
Precios = {1: 200.00,      2: 120.00,    3: 50.00,     4: 350.00}
Stock    = {1: 50,         2: 45,        3: 30,        4: 15}

def mostrar_listado():
    print("========================================")
    print("Lista de Productos:")
    print("========================================")
    for codigo in sorted(Productos.keys()):
        print(f"{codigo} {Productos[codigo]} {Precios[codigo]} {Stock[codigo]}")
    print("========================================")

while True:
    mostrar_listado()
    print("[1] Agregar, [2] Eliminar, [3] Actualizar, [4] Salir")
    opcion = input("Elija opción: ")
    
    if opcion == '1':
        print("\n--- Agregar producto ---")
        try:
            nuevo_codigo = int(input("Ingrese el código del nuevo producto: "))
            # Verificamos si el código ya existe
            if nuevo_codigo in Productos:
                print(f"El código {nuevo_codigo} ya existe. Intente con otro código.")
                continue
            nombre = input("Ingrese el nombre del producto: ")
            precio = float(input("Ingrese el precio del producto: "))
            stock = int(input("Ingrese la cantidad en stock: "))
            
            # Insertamos en los diccionarios
            Productos[nuevo_codigo] = nombre
            Precios[nuevo_codigo] = precio
            Stock[nuevo_codigo] = stock
            print(f"Producto '{nombre}' agregado correctamente.\n")
        except ValueError:
            print("Error: Ingrese datos válidos.\n")
    
    elif opcion == '2':
        print("\n--- Eliminar producto ---")
        try:
            codigo_eliminar = int(input("Ingrese el código del producto a eliminar: "))
            if codigo_eliminar in Productos:
                nombre_eliminado = Productos.pop(codigo_eliminar)
                Precios.pop(codigo_eliminar)
                Stock.pop(codigo_eliminar)
                print(f"Producto '{nombre_eliminado}' eliminado correctamente.\n")
            else:
                print("El código ingresado no existe.\n")
        except ValueError:
            print("Error: Ingrese un código válido.\n")
    
    elif opcion == '3':
        print("\n--- Actualizar producto ---")
        try:
            codigo_actualizar = int(input("Ingrese el código del producto a actualizar: "))
            if codigo_actualizar in Productos:
                nuevo_nombre = input(f"Ingrese el nuevo nombre (o deje vacío para conservar '{Productos[codigo_actualizar]}'): ")
                nuevo_precio = input(f"Ingrese el nuevo precio (o deje vacío para conservar '{Precios[codigo_actualizar]}'): ")
                nuevo_stock = input(f"Ingrese el nuevo stock (o deje vacío para conservar '{Stock[codigo_actualizar]}'): ")

                # Si el usuario deja vacío, mantenemos el valor anterior
                if nuevo_nombre.strip():
                    Productos[codigo_actualizar] = nuevo_nombre
                if nuevo_precio.strip():
                    Precios[codigo_actualizar] = float(nuevo_precio)
                if nuevo_stock.strip():
                    Stock[codigo_actualizar] = int(nuevo_stock)

                print("Producto actualizado correctamente.\n")
            else:
                print("El código ingresado no existe.\n")
        except ValueError:
            print("Error: Ingrese datos válidos.\n")
    
    elif opcion == '4':
        print("Saliendo del programa...")
        break
    
    else:
        print("\nOpción inválida. Intente nuevamente.\n")

print("Programa finalizado.")
