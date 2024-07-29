import unittest
import json
from appAPI import app, tasks

class TodoAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Clear the tasks list and verify it's empty
        global tasks
        print(f"Tasks before clearing: {tasks}")  # Debugging output
        tasks.clear()
        print(f"Tasks after clearing: {tasks}")   # Debugging output
        assert len(tasks) == 0, "Tasks list not cleared properly"

        # Create a task to use in the tests
        response = self.app.post('/tasks', data=json.dumps({
            'title': 'Test Task',
            'description': 'This is a test task'
        }), content_type='application/json')
        print(f"Setup Response: {response.status_code}, Tasks: {tasks}")
        assert response.status_code == 201, "Setup task creation failed"

        # Verify that the task was created
        if tasks:
            print(f"Created Task: {tasks[-1]}")  # Output the created task details
        else:
            print("No task was created during setup.")


    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), "Welcome to the To-Do List API!")

    def test_get_tasks(self):
        response = self.app.get('/tasks')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        data = json.loads(response.data)
        print(f"Get Tasks: {data}")  # Debugging output
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 1)  
        
    def test_create_task(self):
        new_task = {
            'title': 'Another Test Task',
            'description': 'This is another test task'
        }
        response = self.app.post('/tasks', data=json.dumps(new_task), content_type='application/json')
        print(f"Create Task Response: {response.status_code}, Data: {response.data}")  # Debugging output
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['title'], new_task['title'])
        self.assertEqual(data['description'], new_task['description'])
        self.assertEqual(data['completed'], False)

    def test_get_task(self):
        response = self.app.get('/tasks/1')
        print(f"Get Task: {response.status_code}, Data: {response.data}")  # Debugging output
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['title'], 'Test Task')

    def test_update_task(self):
        updated_task = {
            'title': 'Updated Task',
            'description': 'This is an updated test task',
            'completed': True
        }
        response = self.app.put('/tasks/1', data=json.dumps(updated_task), content_type='application/json')
        print(f"Update Task Response: {response.status_code}, Data: {response.data}")  # Debugging output
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['title'], updated_task['title'])
        self.assertEqual(data['description'], updated_task['description'])
        self.assertEqual(data['completed'], True)

    def test_delete_task(self):
        response = self.app.delete('/tasks/1')
        print(f"Delete Task Response: {response.status_code}, Data: {response.data}")  # Debugging output
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Task deleted')

    def test_task_not_found(self):
        response = self.app.get('/tasks/999')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Task not found')

if __name__ == '__main__':
    unittest.main()
