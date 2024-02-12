from flask import Flask

# Routes Importando los Blueprints
from .route import Api_task

app = Flask(__name__)


def init_app(config):

    # Configuration
    app.config.from_object(config)

    # Blueprints
    app.register_blueprint(Api_task.ApiRestfull)

    return app