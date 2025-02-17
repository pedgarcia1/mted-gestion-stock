from flask import Flask, render_template, request, redirect, url_for, Response
from waitress import serve
import db_sqlite as db

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        # Obtén los datos enviados por el formulario:
        part_number = request.form.get('part_number')
        stock = request.form.get('stock')
        justificacion = request.form.get('justificacion')
        modificado_por = request.form.get('modificado_por')
        
        # Aquí es donde deberías ejecutar la función de la base de datos que ya tienes creada.
        # Por ejemplo, si tienes una función llamada "guardar_item" podrías llamarla de esta forma:
        # guardar_item(part_number, stock, justificacion, modificado_por)
        # print(part_number, stock, justificacion, modificado_por)
        db.modificacion(part_number, stock, justificacion, modificado_por)
        
        # Luego redirige o muestra un mensaje de éxito:
        return redirect(url_for('index'))
    
    # Si la solicitud es GET, simplemente renderiza el formulario:
    return render_template('add_item.html')

@app.route('/alta_item', methods=['GET', 'POST'])
def alta_item():
    if request.method == 'POST':
        # Obtén los datos enviados por el formulario:
        part_number = request.form.get('part_number')
        part_name = request.form.get('part_name')
        fabricante = request.form.get('fabricante')
        modelo = request.form.get('modelo')
        rubro = request.form.get('rubro')
        almacen = request.form.get('almacen')
        stock = request.form.get('stock')
        stock_minimo = request.form.get('stock_minimo')
        unidad = request.form.get('unidad')
        foto = "imagenes/template.png"
        modificado_por = request.form.get('modificado_por')
        costo = request.form.get('costo')
        ubicacion = request.form.get('ubicacion')
        
        db.alta_item(part_number,part_name,fabricante,modelo,rubro,almacen,stock,stock_minimo,unidad,foto,modificado_por,costo,ubicacion)
        
        # Luego redirige o muestra un mensaje de éxito:
        return redirect(url_for('index'))
    
    elif request.method == 'GET':
        # Si la solicitud es GET, simplemente renderiza el formulario:
        return render_template('alta_item.html')
    
@app.route('/baja_item', methods=['GET', 'POST'])
def baja_item():
    if request.method == 'POST':
        # Obtén los datos enviados por el formulario:
        part_number = request.form.get('part_number')
        modificado_por = request.form.get('modificado_por')
        
        db.baja_item(part_number)
        
        # Luego redirige o muestra un mensaje de éxito:
        return redirect(url_for('index'))
    
    elif request.method == 'GET':
        # Si la solicitud es GET, simplemente renderiza el formulario:
        return render_template('baja_item.html')
    

@app.route('/list_items',methods=['GET'])
def list_items():
    if request.method == 'GET':
        items = db.get_items()  # Función que retorna la lista de filas de la tabla
        return render_template('list_items.html', items=items)

@app.route('/list_movimientos',methods=['GET'])
def list_movimientos():
    if request.method == 'GET':
        movimientos = db.get_movimientos()  # Función que retorna la lista de filas de la tabla
        return render_template('list_movimientos.html', movimientos=movimientos)
    
@app.route('/descargar_items_csv', methods=['GET'])
def descargar_items_csv():
    # Llama a la función que genera el CSV y obtiene el contenido
    csv_data = db.items_to_csv()  
    # Devuelve el CSV como archivo descargable
    return Response(
        csv_data,
        mimetype='text/csv',
        headers={
            "Content-disposition":
            "attachment; filename=items.csv"
        }
    )
    
@app.route('/descargar_movimientos_csv', methods=['GET'])
def descargar_movimientos_csv():
    # Llama a la función que genera el CSV y obtiene el contenido
    csv_data = db.movimientos_to_csv()  
    # Devuelve el CSV como archivo descargable
    return Response(
        csv_data,
        mimetype='text/csv',
        headers={
            "Content-disposition":
            "attachment; filename=movimientos.csv"
        }
    )

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)