from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory database for simplicity
tasks = []

# Root endpoint
@app.route('/')
def home():
    return "Welcome to the To-Do List API!"

# Endpoint to retrieve all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

# Endpoint to retrieve a single task by ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task:
        return jsonify(task)
    return jsonify({'message': 'Task not found'}), 404

# Endpoint to create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    task_data = request.json
    new_task = {
        'id': len(tasks) + 1,
        'title': task_data['title'],
        'description': task_data.get('description', ''),
        'completed': False
    }
    tasks.append(new_task)
    return jsonify(new_task), 201

# Endpoint to update an existing task by ID
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task:
        task_data = request.json
        task['title'] = task_data.get('title', task['title'])
        task['description'] = task_data.get('description', task['description'])
        task['completed'] = task_data.get('completed', task['completed'])
        return jsonify(task)
    return jsonify({'message': 'Task not found'}), 404

# Endpoint to delete a task by ID
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return jsonify({'message': 'Task deleted'})

# Optional: Handle favicon requests
@app.route('/favicon.ico')
def favicon():
    return '', 204  # Return no content for favicon requests

if __name__ == '__main__':
    app.run(debug=True)
