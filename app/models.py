from datetime import datetime
from app import db

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='planning') # planning, in_progress, completed, on_hold, cancelled
    
    tasks = db.relationship('Task', backref='project', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Project {self.name}>'
    
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    start_date = db.Column(db.DateTime, nullable=True)
    complete_date = db.Column(db.DateTime, nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='todo') # pending, in_progress, completed, blocked, cancelled
    priority = db.Column(db.String(50), nullable=False, default='medium') # low, medium, high
    estimated_hours = db.Column(db.Float, nullable=True)
    actual_hours = db.Column(db.Float, nullable=True)
    asigned_to = db.Column(db.String(100), nullable=True)  # User or team assigned to the task
    tags = db.Column(db.String(200), nullable=True)  # Comma-separated tags

    
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    dependencies = db.relationship('TaskDependency', foreign_keys='TaskDependency.task_id', backref='task', lazy=True, cascade='all, delete-orphan')
    dependent_tasks = db.relationship('TaskDependency', foreign_keys='TaskDependency.dependent_task_id', backref='dependent_task', lazy=True, cascade='all, delete-orphan')     
 
    def __repr__(self):
        return f'<Task {self.title}>'
    
class TaskDependency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    dependent_task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<TaskDependency {self.task_id} -> {self.dependent_task_id}>'