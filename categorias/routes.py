from flask import Blueprint, render_template, request, redirect, url_for
from database import get_connection

categorias_bp = Blueprint('categorias', __name__, template_folder='templates')

@categorias_bp.route('/categorias')
def listar():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM categorias ORDER BY nome')
    categorias = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('lista.html', categorias=categorias)

@categorias_bp.route('/categorias/nova', methods=['GET', 'POST'])
def nova():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form.get('descricao', '')
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO categorias (nome, descricao) VALUES (%s, %s)',
            (nome, descricao)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('categorias.listar'))
    return render_template('form.html', categoria=None)

@categorias_bp.route('/categorias/<int:id>/editar', methods=['GET', 'POST'])
def editar(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form.get('descricao', '')
        cursor.execute(
            'UPDATE categorias SET nome = %s, descricao = %s WHERE id = %s',
            (nome, descricao, id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('categorias.listar'))
    
    cursor.execute('SELECT * FROM categorias WHERE id = %s', (id,))
    categoria = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('form.html', categoria=categoria)

@categorias_bp.route('/categorias/<int:id>/excluir', methods=['POST'])
def excluir(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM categorias WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('categorias.listar'))