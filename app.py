from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///todos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), default='')
    category = db.Column(db.String(50), default='General')
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'completed': self.completed,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M')
        }

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/todos', methods=['GET'])
def get_todos():
    category = request.args.get('category', '')
    status = request.args.get('status', 'all')
    query = Todo.query
    if category:
        query = query.filter_by(category=category)
    if status == 'active':
        query = query.filter_by(completed=False)
    elif status == 'completed':
        query = query.filter_by(completed=True)
    todos = query.order_by(Todo.created_at.desc()).all()
    return jsonify([t.to_dict() for t in todos])

@app.route('/api/todos', methods=['POST'])
def create_todo():
    data = request.json
    if not data or not data.get('title', '').strip():
        return jsonify({'error': 'Title is required'}), 400
    todo = Todo(
        title=data['title'].strip(),
        description=data.get('description', '').strip(),
        category=data.get('category', 'General')
    )
    db.session.add(todo)
    db.session.commit()
    return jsonify(todo.to_dict()), 201

@app.route('/api/todos/<int:todo_id>', methods=['PATCH'])
def update_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    data = request.json
    if 'completed' in data:
        todo.completed = data['completed']
    if 'title' in data:
        todo.title = data['title'].strip()
    if 'description' in data:
        todo.description = data['description'].strip()
    if 'category' in data:
        todo.category = data['category']
    db.session.commit()
    return jsonify(todo.to_dict())

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Deleted'})

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
