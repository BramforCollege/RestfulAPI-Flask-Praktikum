from flask import Flask, request, jsonify
from database import get_db, init_db, close_db
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
with app.app_context():
    init_db()

@app.teardown_appcontext
def close_db_error(error):
    """Menjamin koneksi database ditutup setelah request selesai."""
    close_db(error)

@app.route('/api/users', methods=['GET'])
def get_users():
    """Mengambil semua daftar user."""
    db = get_db()
    users = db.execute('SELECT * FROM users').fetchall()
    return jsonify([dict(u) for u in users])

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Mengambil satu user berdasarkan ID."""
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    if user:
        return jsonify(dict(user))
    return jsonify({'error': 'User tidak ditemukan'}), 404

@app.route('/api/users', methods=['POST'])
def create_user():
    """Membuat user baru dengan validasi data."""
    data = request.get_json()
    
    # Validasi input
    if not data or 'name' not in data or 'age' not in data:
        return jsonify({'error': 'Field name dan age wajib diisi'}), 400
    
    db = get_db()
    cursor = db.execute(
        'INSERT INTO users (name, age) VALUES (?, ?)', 
        (data['name'], data['age'])
    )
    db.commit()
    
    new_user = {
        'id': cursor.lastrowid,
        'name': data['name'],
        'age': data['age']
    }
    return jsonify(new_user), 201

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Memperbarui data user yang sudah ada."""
    data = request.get_json()
    
    if not data or 'name' not in data or 'age' not in data:
        return jsonify({'error': 'Field name dan age wajib diisi'}), 400

    db = get_db()
    result = db.execute(
        'UPDATE users SET name = ?, age = ? WHERE id = ?', 
        (data['name'], data['age'], user_id)
    )
    
    if result.rowcount == 0:
        return jsonify({'error': 'User tidak ditemukan'}), 404
        
    db.commit()
    return jsonify({'message': 'User berhasil diupdate', 'id': user_id})

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Menghapus user berdasarkan ID."""
    db = get_db()
    result = db.execute('DELETE FROM users WHERE id = ?', (user_id,))
    
    if result.rowcount == 0:
        return jsonify({'error': 'User tidak ditemukan'}), 404
        
    db.commit()
    return jsonify({'message': 'User berhasil dihapus'})

if __name__ == '__main__':
    app.run(debug=True)