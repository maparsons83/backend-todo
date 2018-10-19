import datetime
import logging
import logging.handlers

import requests
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

from initialize import app, api


"""custom logger"""
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.handlers.RotatingFileHandler(
    'todo_logs.log', mode='a', maxBytes=2000, backupCount=5)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

app.config['BUNDLE_ERRORS']=True

TODOS = {
    'todo1': {'title': 'build an API',
              'creation_date': '01/01/2018',
              'last_updated': '01/02/2018',
              'due_date': '01/03/2018',
              'completed': 'True',
              'completed_date': '01/03/2018'},
    'todo2': {'title': 'Do a thing',
              'creation_date': '02/01/2018',
              'last_updated': '02/02/2018',
              'due_date': '02/03/2018',
              'completed': 'False',
              'completed_date': '02/03/2018'},
    'todo3': {'title': 'Do another thing',
              'creation_date': '03/01/2018',
              'last_updated': '03/02/2018',
              'due_date': '03/03/2018',
              'completed': 'True',
              'completed_date': '03/03/2018'},
}

parser = reqparse.RequestParser()
parser.add_argument('title', required=True, help='Title is required')
parser.add_argument('due_date')
parser.add_argument('completed')


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        """
        Aborts process if todo is not found.
        """
        logger.error({'message': 'Todo {} does not exist'.format(todo_id)})
        abort(404, message="Todo {} doesn't exist".format(todo_id))


class Todo(Resource):

    def get(self, todo_id):
        """
        Gets todo item by todo ID
        """
        abort_if_todo_doesnt_exist(todo_id)
        logger.info({'message': 'Todo item {} displayed'.format(TODOS[todo_id])})
        return TODOS[todo_id]

    def delete(self, todo_id):
        """
        Deletes todo item by ID
        """
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        logger.info({'message': 'Todo {} deleted'.format(todo_id)})
        return '', 204

    def put(self, todo_id):
        """
        Updates todo based on argument passed
        """
        args = parser.parse_args()
        for key, value in args.items():
            if value == '':
                continue
            else:
                TODOS[todo_id][key] = value
                TODOS[todo_id]['last_updated'] = str(datetime.datetime.now())
        logger.info({'message': 'Todo {} updated'.format(todo_id)})
        return {todo_id: TODOS[todo_id]}, 200


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        logger.info({'message': 'All todos shown'})
        return TODOS

    def create_todo(self, title, due_date, completed):
        """
        creates todo and sets up defaults for fields.
        Function is used to structure Put request
        """
        new_todo = {}
        new_todo['title'] = title
        new_todo['due_date'] = due_date
        new_todo['completed'] = completed
        new_todo['last_updated'] = datetime.datetime.now().isoformat()
        new_todo['completed_date'] = None
        new_todo['creation_date'] = datetime.datetime.now().isoformat()

        return new_todo

    def post(self):
        """
        Posts new todo item to dict
        """
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = self.create_todo(
            args['title'],
            args['due_date'],
            args['completed'],
        )
        logger.info({'message': 'New todo created with ID {}'.format(todo_id)})
        return TODOS[todo_id], 201


# Actually setup the Api resource routing here
api.add_resource(TodoList, '/todosList')
api.add_resource(Todo, '/todosList/<todo_id>')


if __name__ == '__main__':
    app.run(debug=True)
