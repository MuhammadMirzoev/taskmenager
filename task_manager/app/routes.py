from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from werkzeug.exceptions import BadRequest
from .models import Task
from .db import db

# ---------------- API Blueprint ----------------
task_bp = Blueprint("task_bp", __name__)

@task_bp.post("/tasks")
def create_task():
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
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict())

@task_bp.get("/tasks")
def list_tasks():
    tasks = Task.query.order_by(Task.id.asc()).all()
    return jsonify([t.to_dict() for t in tasks])

@task_bp.put("/tasks/<int:task_id>")
def update_task(task_id: int):
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
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully"})


# ---------------- Web Blueprint ----------------
site_bp = Blueprint("site_bp", __name__)

@site_bp.route("/", methods=["GET"])
def index():
    tasks = Task.query.order_by(Task.id.asc()).all()
    return render_template("index.html", tasks=tasks)

@site_bp.route("/create", methods=["POST"])
def create():
    title = request.form.get("title")
    description = request.form.get("description", "")
    if not title:
        flash("Title is required!", "error")
        return redirect(url_for("site_bp.index"))
    task = Task(title=title, description=description)
    db.session.add(task)
    db.session.commit()
    flash("Task created successfully!", "success")
    return redirect(url_for("site_bp.index"))

@site_bp.route("/update/<int:task_id>", methods=["POST"])
def update(task_id):
    task = Task.query.get_or_404(task_id)
    title = request.form.get("title")
    description = request.form.get("description", "")
    status = request.form.get("status", "pending")
    if not title:
        flash("Title cannot be empty!", "error")
        return redirect(url_for("site_bp.index"))
    task.title = title
    task.description = description
    task.status = status
    db.session.commit()
    flash("Task updated successfully!", "success")
    return redirect(url_for("site_bp.index"))

@site_bp.route("/delete/<int:task_id>", methods=["POST"])
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted successfully!", "success")
    return redirect(url_for("site_bp.index"))
