from flask import Flask, render_template
from flasgger import Swagger
from .db import db
from .routes import task_bp, site_bp  # подключаем оба blueprint-а

def create_app(testing: bool = False):
    app = Flask(__name__)

    # Настройки базы данных
    db_uri = "sqlite:///:memory:" if testing else "sqlite:///tasks.db"
    app.config.update(
        SQLALCHEMY_DATABASE_URI=db_uri,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JSON_SORT_KEYS=False,
        TESTING=testing,
        SECRET_KEY="supersecretkey"  # нужно для flash сообщений
    )

    # Инициализация расширений
    db.init_app(app)
    Swagger(app)

    # Регистрация blueprint-ов
    app.register_blueprint(task_bp, url_prefix="/api")  # API endpoints
    app.register_blueprint(site_bp)                     # Web endpoints

    # Создание таблиц
    with app.app_context():
        db.create_all()

    # Дополнительные маршруты
    @app.get("/health")
    def health():
        """Health check endpoint.
        ---
        tags: [system]
        responses:
          200:
            description: OK
        """
        return {"status": "ok"}

    return app
