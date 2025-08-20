from flask import Flask
from flasgger import Swagger
from .db import db
from .routes import task_bp

def create_app(testing: bool = False):
    app = Flask(__name__)
    db_uri = "sqlite:///:memory:" if testing else "sqlite:///tasks.db"
    app.config.update(
        SQLALCHEMY_DATABASE_URI=db_uri,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JSON_SORT_KEYS=False,
        TESTING=testing,
    )

    # init extensions
    db.init_app(app)
    Swagger(app)

    # register blueprints
    app.register_blueprint(task_bp, url_prefix="/api")

    # create tables
    with app.app_context():
        db.create_all()

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
