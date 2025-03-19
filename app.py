"""A simple CRUD application for managing space station resources."""
from flask import Flask, g, jsonify, request
import sqlite3

app = Flask(__name__)
app.config['DATABASE'] = 'mars_resources.db'

def get_db():
    """Connect to the application's configured database.

    The connection is stored in the application context.
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Closes the database again at the end of the request."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/resources', methods=['GET'])
def get_resources():
    """Returns a list of all resources."""
    db = get_db()
    cursor = db.execute('SELECT * FROM resources')
    resources = cursor.fetchall()
    return jsonify([dict(resource) for resource in resources])

@app.route('/resources/<int:resource_id>', methods=['GET'])
def get_resource(resource_id):
    """Returns a specific resource by ID."""
    db = get_db()
    cursor = db.execute('SELECT * FROM resources WHERE id = ?', (resource_id,))
    resource = cursor.fetchone()
    if resource is None:
        return jsonify({'error': 'Resource not found'}), 404
    return jsonify(dict(resource))

@app.route('/resources', methods=['POST'])
def create_resource():
    """Creates a new resource."""
    data = request.get_json()
    if not data or 'name' not in data or 'quantity' not in data:
        return jsonify({'error': 'Missing name or quantity'}), 400
    db = get_db()
    cursor = db.execute(
        'INSERT INTO resources (name, quantity) VALUES (?, ?)',
        (data['name'], data['quantity'])
    )
    db.commit()
    return jsonify(
        {'id': cursor.lastrowid, 'name': data['name'], 'quantity': data['quantity']}
    ), 201

@app.route('/resources/<int:resource_id>', methods=['PUT'])
def update_resource(resource_id):
    """Updates an existing resource by ID."""
    data = request.get_json()
    if not data or 'name' not in data or 'quantity' not in data:
        return jsonify({'error': 'Missing name or quantity'}), 400
    db = get_db()
    cursor = db.execute(
        'UPDATE resources SET name = ?, quantity = ? WHERE id = ?',
        (data['name'], data['quantity'], resource_id)
    )
    db.commit()
    if cursor.rowcount == 0:
        return jsonify({'error': 'Resource not found'}), 404
    return jsonify(
        {'id': resource_id, 'name': data['name'], 'quantity': data['quantity']}
    )

@app.route('/resources/<int:resource_id>', methods=['DELETE'])
def delete_resource(resource_id):
    """Deletes a resource by ID."""
    db = get_db()
    cursor = db.execute('DELETE FROM resources WHERE id = ?', (resource_id,))
    db.commit()
    if cursor.rowcount == 0:
        return jsonify({'error': 'Resource not found'}), 404
    return jsonify({'message': 'Resource deleted'})

if __name__ == '__main__':
    """Runs the Flask application if the script is executed directly."""
    app.run(debug=True)