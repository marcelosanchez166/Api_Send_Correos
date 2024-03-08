from flask import Flask

# Routes Importando los Blueprints
from .route import Api_task,authtokenJWT





app = Flask(__name__)



def init_app(config):
    # Configuration
    app.config.from_object(config)
    # Blueprints
    app.register_blueprint(Api_task.ApiRestfull )
    app.register_blueprint(authtokenJWT.jwt_token_acces )
    return app