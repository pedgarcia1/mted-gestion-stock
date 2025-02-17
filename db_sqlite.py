import sqlite3
from datetime import datetime
import csv
import io

def modificacion(part_number, operacion_stock, justificacion, creado_por, conexion=None, cursor=None):
    
    creo_conexion = False
    if conexion is None and cursor is None:
        [conexion, cursor] = create_connection()
        creo_conexion = True
    
    # Insertar el movimiento
    sql_insert_movimiento = """
        INSERT INTO movimientos (part_number, operacion_stock, justificacion, creado_por, fecha)
        VALUES (?, ?, ?, ?, ?)
    """
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    valores_mov = (part_number, operacion_stock, justificacion, creado_por, fecha)
    cursor.execute(sql_insert_movimiento, valores_mov)
    
    # Hacer commit
    conexion.commit()
    
    # Cierro la conexion solo si se creo en esta funcion
    if creo_conexion:
        conexion.close()

    
def alta_item(part_number,part_name,fabricante,modelo,rubro,almacen,stock,stock_minimo,unidad,foto,modificado_por,costo,ubicacion):
    # Creo conexion
    [conexion, cursor] = create_connection()
    # Creo item
    sql_insert_item = """
    INSERT INTO items (part_number, part_name, fabricante, modelo, rubro, almacen, stock, stock_minimo, unidad, foto, ultima_modificacion, modificado_por, costo, ubicacion, estado)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """
    valores_item = (part_number, part_name, fabricante, modelo, rubro, almacen, 0, stock_minimo, unidad, foto, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), modificado_por, costo, ubicacion, 'ACTIVO')
    cursor.execute(sql_insert_item, valores_item)
    conexion.commit()
    # Commite para dar de alta el item
    # Registro el movimiento en la tabla movimientos
    modificacion(part_number,stock,"Alta",modificado_por,conexion,cursor)
    conexion.close()


# BAJA
# 1. Stock a cero
# 2. Cambiar estado a 'BAJA'
def baja_item(part_number,modificado_por):
    [conexion, cursor] = create_connection()
    # Stock a cero
    stock = get_stock(part_number)
    if stock is not None:
        # Ajustar stock a 0 con un movimiento
        modificacion(part_number, -stock, "Baja", modificado_por)
        # Cambiar estado a 'BAJA'
        cursor.execute("""
            UPDATE items
            SET estado = 'BAJA'
            WHERE part_number = ?
        """, (part_number,))
        conexion.commit()
    conexion.close()
    
def download_items_csv():
    [conexion, cursor] = create_connection()
    cursor.execute("SELECT * FROM items")
    with open("items.csv", "w", newline="") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)
    conexion.close()
    
def items_to_csv():
    [conexion, cursor] = create_connection()
    cursor.execute("SELECT * FROM items")
    
    output = io.StringIO()
    csv_writer = csv.writer(output, lineterminator='\n')
    header = [desc[0] for desc in cursor.description]
    csv_writer.writerow(header)
    
    for row in cursor.fetchall():
        csv_writer.writerow(row)
    
    conexion.close()
    return output.getvalue()
    
def get_items():
    [conexion, cursor] = create_connection()
    conexion.row_factory = sqlite3.Row  # Permite acceder a las columnas por nombre
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM items WHERE estado = 'ACTIVO'")
    # Convertir cada fila a un diccionario para que sea compatible con el template
    items = [dict(row) for row in cursor.fetchall()]
    conexion.close()
    return items

def get_movimientos():
    [conexion, cursor] = create_connection()
    conexion.row_factory = sqlite3.Row  # Permite acceder a las columnas por nombre
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM movimientos")
    # Convertir cada fila a un diccionario para que sea compatible con el template
    movimientos = [dict(row) for row in cursor.fetchall()]
    conexion.close()
    return movimientos

def movimientos_to_csv():
    [conexion, cursor] = create_connection()
    cursor.execute("SELECT * FROM movimientos")
    
    output = io.StringIO()
    csv_writer = csv.writer(output, lineterminator='\n')
    
    header = [desc[0] for desc in cursor.description]
    csv_writer.writerow(header)
    
    for row in cursor.fetchall():
        csv_writer.writerow(row)
    
    conexion.close()
    return output.getvalue()
        
def download_movimientos_csv():
    [conexion, cursor] = create_connection()
    cursor.execute("SELECT * FROM movimientos")
    with open("movimientos.csv", "w", newline="") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)
    conexion.close()
    
def get_stock(part_number):
    [conexion, cursor] = create_connection()
    cursor.execute("SELECT stock FROM items WHERE part_number = ?", (part_number,))
    stock = cursor.fetchone()
    conexion.close()
    return stock[0]

def get_item(part_number):
    [conexion, cursor] = create_connection()
    cursor.execute("SELECT * FROM items WHERE part_number = ?", (part_number,))
    item = cursor.fetchone()
    conexion.close()
    return item
        
def create_connection():
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    
    # Crear tabla items (si no existe)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        part_number INTEGER NOT NULL UNIQUE,
        part_name TEXT,
        fabricante TEXT,
        modelo TEXT,
        rubro TEXT,
        almacen TEXT,
        stock INTEGER NOT NULL DEFAULT 0,
        stock_minimo INTEGER NOT NULL DEFAULT 0,
        unidad TEXT,
        foto TEXT,
        ultima_modificacion TEXT,
        modificado_por TEXT,
        costo REAL,
        ubicacion TEXT,
        estado TEXT DEFAULT 'ACTIVO'
    );
    """)

    # Crear tabla movimientos (si no existe)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movimientos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        part_number TEXT NOT NULL,
        operacion_stock INTEGER NOT NULL,
        justificacion TEXT,
        creado_por TEXT,
        fecha TEXT NOT NULL,
        FOREIGN KEY (part_number) REFERENCES items(part_number)
    );
    """)

    # Crear el trigger
    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS update_stock_after_movement
    AFTER INSERT ON movimientos
    FOR EACH ROW
    BEGIN
        UPDATE items
        SET stock = stock + NEW.operacion_stock,
            ultima_modificacion = CURRENT_TIMESTAMP,
            modificado_por = NEW.creado_por
        WHERE part_number = NEW.part_number;
    END;
    """)

    conexion.commit()
    return conexion, cursor
    
# gl
