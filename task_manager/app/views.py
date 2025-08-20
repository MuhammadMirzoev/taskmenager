from flask import Blueprint, render_template, request, redirect, url_for
from app.models import db, Task

views_bp = Blueprint("views", __name__)

@views_bp.route("/")
def index():
    tasks = Task.query.all()
    return render_template("index.html", tasks=tasks)

@views_bp.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title")
    description = request.form.get("description")
    status = request.form.get("status", "pending")

    if title:
        task = Task(title=title, description=description, status=status)
        db.session.add(task)
        db.session.commit()
    return redirect(url_for("views.index"))

@views_bp.route("/update/<int:task_id>/<string:status>")
def update_task(task_id, status):
    task = Task.query.get_or_404(task_id)
    task.status = status
    db.session.commit()
    return redirect(url_for("views.index"))

@views_bp.route("/delete/<int:task_id>")
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("views.index"))
