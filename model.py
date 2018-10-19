from flask_restful import fields, marshal_with, Resource

resource_fields = {
    'title':   fields.String,
    'creation_date':    fields.DateTime(dt_format='rfc822'),
    'last_updated':    fields.String,
    'due_date': fields.DateTime(dt_format='rfc822'),
    'completed': fields.String,
    'uri':    fields.Url('todo_ep'),
}


class TodoDao(object):
    def __init__(self, todo_id, title, last_updated,
                 due_date=None, completed=False):
        self.todo_id = todo_id
        self.title = title
        self.due_date = due_date
        self.last_updated = last_updated
        self.completed = completed
        # This field will not be sent in the response
        self.status = 'active'


class Todo(Resource):
    @marshal_with(resource_fields)
    def get(self, **kwargs):
        return TodoDao(todo_id='my_todo', task='Remember the milk')
