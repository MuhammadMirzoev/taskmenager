from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest
from .models import Task
from .db import db

task_bp = Blueprint("task_bp", __name__)

@task_bp.post("/tasks")
def create_task():
    """
    Create a task
    ---
    tags: [tasks]
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              title:
                type: string
              description:
                type: string
              status:
                type: string
            required: [title]
    responses:
      201:
        description: Created
        content:
          application/json:
            schema:
              type: object
              properties:
                id: {type: integer}
                title: {type: string}
                description: {type: string}
                status: {type: string}
      400:
        description: Bad Request
    """
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    if not title:
        raise BadRequest("Field 'title' is required.")
    task = Task(
        title=title,
        description=data.get("description", ""),
        status=data.get("status", "pending"),
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

@task_bp.get("/tasks/<int:task_id>")
def get_task(task_id: int):
    """
    Get task by ID
    ---
    tags: [tasks]
    parameters:
      - in: path
        name: task_id
        schema: {type: integer}
        required: true
    responses:
      200:
        description: Task object
      404:
        description: Not Found
    """
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict())

@task_bp.get("/tasks")
def list_tasks():
    """
    Get tasks list
    ---
    tags: [tasks]
    responses:
      200:
        description: List of tasks
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
    """
    tasks = Task.query.order_by(Task.id.asc()).all()
    return jsonify([t.to_dict() for t in tasks])

@task_bp.put("/tasks/<int:task_id>")
def update_task(task_id: int):
    """
    Update a task
    ---
    tags: [tasks]
    parameters:
      - in: path
        name: task_id
        schema: {type: integer}
        required: true
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              title: {type: string}
              description: {type: string}
              status: {type: string}
    responses:
      200:
        description: Updated
      404:
        description: Not Found
    """
    task = Task.query.get_or_404(task_id)
    data = request.get_json(silent=True) or {}
    if "title" in data:
        if not data["title"]:
            raise BadRequest("Field 'title' cannot be empty.")
        task.title = data["title"]
    if "description" in data:
        task.description = data["description"] or ""
    if "status" in data:
        task.status = data["status"]
    db.session.commit()
    return jsonify(task.to_dict())

@task_bp.delete("/tasks/<int:task_id>")
def delete_task(task_id: int):
    """
    Delete a task
    ---
    tags: [tasks]
    parameters:
      - in: path
        name: task_id
        schema: {type: integer}
        required: true
    responses:
      200:
        description: Deleted
      404:
        description: Not Found
    """
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully"})
