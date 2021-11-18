from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Task(db.Model):
    """Tasks for the To-Do list."""
    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.String(250), nullable =False)
    description = db.Column(db.Text)
    completed = db.Column(db.Boolean, default=False)

    # def __init__(self, id, name,description,completed):
    #     self.id = id
    #     self.name = name
    #     self.description = description
    #     self.completed = completed

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"{self.name}"
