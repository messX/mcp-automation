from flask import Blueprint, request, jsonify
from .models import Task, Project, TaskDependency
from . import db
from .schemas import task_schema, tasks_schema, project_schema, projects_schema, task_dependency_schema, task_dependencies_schema

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/projects', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    return projects_schema.jsonify(projects)

@bp.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    project = Project.query.get_or_404(project_id)
    return project_schema.jsonify(project)  

@bp.route('/projects', methods=['POST'])
def create_project():
    data = request.get_json()
    project = Project(
        name=data.get('name'),
        description=data.get('description'),
        start_date=data.get('start_date', None),
        end_date=data.get('end_date', None),
        status=data.get('status', 'planning')  # Default status is 'planning'
    )
    db.session.add(project)
    db.session.commit()
    return project_schema.jsonify(project), 201

@bp.route('/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id): 
    project = Project.query.get_or_404(project_id)
    data = request.get_json()
    project = project_schema.load(data, instance=project, partial=True)
    db.session.commit()
    return project_schema.jsonify(project)

@bp.route('/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id): 
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return jsonify({'message': 'Project deleted successfully'}), 204

@bp.route('/projects/<int:project_id>/tasks', methods=['GET'])
def get_project_tasks(project_id):
    project = Project.query.get_or_404(project_id)
    return tasks_schema.jsonify(project.tasks)

@bp.route('/projects/<int:project_id>/tasks', methods=['POST'])
def create_project_task(project_id):
    project = Project.query.get_or_404(project_id)
    data = request.get_json()
    new_task = task_schema.load(data)
    new_task.project = project
    db.session.add(new_task)
    db.session.commit()
    return task_schema.jsonify(new_task), 201

@bp.route('/projects/<int:project_id>/tasks/<int:task_id>', methods=['GET'])
def get_project_task(project_id, task_id):
    project = Project.query.get_or_404(project_id)
    task = Task.query.filter_by(id=task_id, project_id=project.id).first_or_404()
    return task_schema.jsonify(task)

@bp.route('/projects/<int:project_id>/tasks/<int:task_id>', methods=['PUT'])
def update_project_task(project_id, task_id):
    project = Project.query.get_or_404(project_id)
    task = Task.query.filter_by(id=task_id, project_id=project.id).first_or_404()
    data = request.get_json()
    task = task_schema.load(data, instance=task, partial=True)
    db.session.commit()
    return task_schema.jsonify(task)

@bp.route('/projects/<int:project_id>/tasks/<int:task_id>', methods=['DELETE'])
def delete_project_task(project_id, task_id):
    project = Project.query.get_or_404(project_id)
    task = Task.query.filter_by(id=task_id, project_id=project.id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'}), 204

@bp.route('/tasks/<int:task_id>/dependencies', methods=['GET'])
def get_task_dependencies(task_id):
    task = Task.query.get_or_404(task_id)
    return task_dependencies_schema.jsonify(task.dependencies)

@bp.route('/tasks/<int:task_id>/dependencies', methods=['POST'])
def create_task_dependency(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    
    depends_on_task_id = data.get('dependent_task_id')
    if not depends_on_task_id:
        return jsonify({'error': 'dependent_task_id is required'}), 400
    dependent_task = Task.query.get_or_404(depends_on_task_id)
    if task.id == dependent_task.id:
        return jsonify({'error': 'A task cannot depend on itself'}), 400
    elif task.project_id != dependent_task.project_id:
        return jsonify({'error': 'Dependent task must belong to the same project'}), 400

    existing_dependency = TaskDependency.query.filter_by(task_id=task.id, dependent_task_id=dependent_task.id).first()
    if existing_dependency:
        return jsonify({'message': 'Dependency already exists'}), 200
    
    new_dependency = TaskDependency(task_id=task.id, dependent_task_id=dependent_task.id)
    db.session.add(new_dependency)
    db.session.commit()
    return task_dependency_schema.jsonify(new_dependency), 201

@bp.route('/tasks/<int:task_id>/dependencies/<int:dependency_id>', methods=['DELETE'])
def delete_task_dependency(task_id, dependency_id):
    task = Task.query.get_or_404(task_id)
    dependency = TaskDependency.query.filter_by(id=dependency_id, task_id=task.id).first_or_404()
    db.session.delete(dependency)
    db.session.commit()
    return jsonify({'message': 'Task dependency deleted successfully'}), 204

@bp.route('/tasks/<int:task_id>/dependencies/<int:dependency_id>', methods=['GET'])
def get_task_dependency(task_id, dependency_id):
    task = Task.query.get_or_404(task_id)
    dependency = TaskDependency.query.filter_by(id=dependency_id, task_id=task.id).first_or_404()
    return task_dependency_schema.jsonify(dependency)
