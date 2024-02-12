#en este archivo se instancia el metodo init_app del archivo __init__.py que cuenta con los blueprints ademas se crea la instancia de la aplicacion 

from config import config
from app import init_app

configurationdev = config['development']
configurationprod = config['production']

app = init_app(configurationdev)


if __name__ == '__main__':
    app.run()