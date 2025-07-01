from flask import Flask, request, render_template_string
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# Crear base de datos y tabla si no existe
def init_db():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Agregar usuario
def agregar_usuario(nombre, password):
    password_hash = generate_password_hash(password)
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE nombre = ?', (nombre,))
    if not cursor.fetchone():  # Agregar solo si no existe
        cursor.execute('INSERT INTO usuarios (nombre, password_hash) VALUES (?, ?)', (nombre, password_hash))
        conn.commit()
    conn.close()

# Verificar credenciales
def verificar_usuario(nombre, password):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('SELECT password_hash FROM usuarios WHERE nombre = ?', (nombre,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return check_password_hash(result[0], password)
    return False

# HTML básico
formulario_html = '''
<h2>Login de Integrantes</h2>
<form method="POST">
  Nombre: <input type="text" name="nombre"><br>
  Contraseña: <input type="password" name="password"><br>
  <input type="submit" value="Ingresar">
</form>
<p>{{ mensaje }}</p>
'''

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    mensaje = ''
    if request.method == 'POST':
        nombre = request.form['nombre']
        password = request.form['password']
        if verificar_usuario(nombre, password):
            mensaje = f'Bienvenido {nombre} (usuario válido)'
        else:
            mensaje = 'Credenciales incorrectas'
    return render_template_string(formulario_html, mensaje=mensaje)

if __name__ == '__main__':
    init_db()

    # Lista actualizada de integrantes (sin RUT)
    integrantes = {
        'Daniel Pimentel': 'daniel123',
        'Andres Altamirano': 'andres456',
        'Pablo Cabezas': 'pablo789',
        'Diego Tordecilla': 'diego101',
        'Nicolas Gallardo': 'nico2025',
        'Matias Gerrero': 'matias999'
    }

    for nombre, clave in integrantes.items():
        agregar_usuario(nombre, clave)

    app.run(port=5800)
