# import the api requirement ( also make sure that flask-restful is installed in the env)
from flask_restful import Resource, Api , abort
from flask import Flask , request
from models import db,Task
import logging
# Configure the logging module
logging.basicConfig(filename='flask_server_logs.log',filemode='w',level=logging.DEBUG,
format='%(asctime)s %(name)s - %(levelname)s - %(message)s',
datefmt='%d-%b-%y %H:%M:%S')

#configure the app & database
todo_flask_app = Flask(__name__)
todo_flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
todo_flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure Secret Key
todo_flask_app.config['SECRET_KEY'] = '0zx5c34as65d4654&%^#$#$@'

todo_list = [
    {'name': 'a', 'id': 1, 'description': 'study flask'},
    {'name': 'b', 'id': 2, 'description': 'revise django'},
    {'name': 'c', 'id': 3, 'description': 'make a python proj'}
]
# initiate the api
todo_api = Api(todo_flask_app)
# usage create a class for the required resource
class TodoRUD(Resource): # will need an id
    def get(self, **kwargs):
        task_id = kwargs.get('task_id')
        print("id ->", task_id)
        task = Task.query.get(task_id)
        # if not task:
        #     abort(404, message='Not Found')

        data = {
            'id': task.id,
            'name': task.name,
            'description': task.description,
            'completed': task.completed
        }

        return data, 200

    def delete(self, *args, **kwargs):
        task_id = kwargs.get('task_id')
        print("id ->", task_id)
        task_obj = Task.query.get(task_id)

        print('todo obj -> ', task_obj)

        db.session.delete(task_obj)  # delete query
        db.session.commit()

        return {'message': 'Deleted Successfully'}, 200

    def patch(self, **kwargs):  # this method to update the task name only
        task_id = kwargs.get('task_id')
        task = Task.query.get(task_id)
        task.name = request.form.get('name')
        print(task.name)
        db.session.commit()
        task = Task.query.get(task_id)
        data = {
            'id': task.id,
            'name': task.name,
            'description': task.description,
            'completed': task.completed
        }
        return data
    
class TodoLC(Resource): # won't need an id
    def get(self):
        try:
            task_objects = Task.query.filter().all()
            print("TD OBJS -> ", task_objects)
            my_new_list = []

            for task in task_objects:
                data = {
                    'id': task.id,
                    'name': task.name,
                    'description': task.description,
                    'completed': task.completed
                }

                my_new_list.append(data)

            return my_new_list

        except Exception as e:
            abort(500, message="Internal Server Error {}".format(e))

    def post(self):

        try:
            data = {
                'name': request.form.get('name'),
                'description': request.form.get('description'),
                'completed': False
            }

            task_obj = Task(**data)  # create object of Task
            db.session.add(task_obj)  # insert query inside the db
            db.session.commit()  # commit to db

            return {'message': 'Task Created Successfully'}, 201
        except Exception as e:
            abort(500, message='Internal Server Error')




# register the resource
todo_api.add_resource(TodoRUD,'/todo<int:task_id>')
todo_api.add_resource(TodoLC,'/todo')

#create db tables
db.init_app(todo_flask_app)  # register sqlalchemy on app
@todo_flask_app.before_first_request # search for db if not exist make a creation
def initiate_database():
    db.create_all()

# run server
todo_flask_app.run(port=5000 , debug=True)
