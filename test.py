import db_sqlite

[conexion, cursor] = db_sqlite.create_connection()

# Consultar items
cursor.execute("SELECT * FROM items")
print(cursor.fetchall())

# Consultar movimientos
cursor.execute("SELECT * FROM movimientos")
print(cursor.fetchall())

# Agregar un item de ejemplo
#         alta_item(part_number,part_name,fabricante,modelo,rubro,almacen,stock,stock_minimo,unidad,foto,modificado_por,costo,ubicacion)
db_sqlite.alta_item("1234567","Item de ejemplo","Fabricante","Modelo","Rubro","Almacen",10,5,"Unidad","foto.jpg","Usuario",100,"Ubicacion")

# agregar stock
db_sqlite.modificacion("1234567",5,"Compra","Usuario")

# consultar stock
print(db_sqlite.get_stock("1234567"))

# consultar item
print(db_sqlite.get_item("1234567"))
item = db_sqlite.get_item("1234567")
id = item[0]
part_number = item[1]
part_name = item[2]
fabricante = item[3]
modelo = item[4]
rubro = item[5]
almacen = item[6]
stock = item[7]
stock_minimo = item[8]
unidad = item[9]
foto = item[10]
fecha_alta = item[11]
modificado_por = item[12]
costo = item[13]
ubicacion = item[14]
estado = item[15]

cursor.execute("SELECT * FROM movimientos")
print(cursor.fetchall())

# baja item
db_sqlite.baja_item("1234567","Usuario")

# consultar
print(db_sqlite.get_stock("1234567"))

cursor.execute("SELECT * FROM movimientos")
print(cursor.fetchall())

conexion.close()