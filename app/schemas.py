from app import ma
from app.models import Project, Task, TaskDependency

class ProjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Project
        load_instance = True
        include_fk = True
        ordered = True
    tasks = ma.Nested('TaskSchema', many=True, exclude=('project_id',))

class TaskSchema(ma.SQLAlchemyAutoSchema):
    project_id = ma.auto_field(dump_only=True)
    class Meta:
        model = Task
        load_instance = True
        include_fk = True
        ordered = True
    dependencies = ma.Nested('TaskDependencySchema', many=True, exclude=('task',))
    dependent_tasks = ma.Nested('TaskDependencySchema', many=True, exclude=('dependent_task',))

class TaskDependencySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TaskDependency
        load_instance = True
        include_fk = True
        ordered = True
    task = ma.Nested(TaskSchema, only=('id', 'name'))
    dependent_task = ma.Nested(TaskSchema, only=('id', 'name'))

project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)    
task_dependency_schema = TaskDependencySchema()
task_dependencies_schema = TaskDependencySchema(many=True)