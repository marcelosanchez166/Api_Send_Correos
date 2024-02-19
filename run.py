#en este archivo se instancia el metodo init_app del archivo __init__.py que cuenta con los blueprints ademas se crea la instancia de la aplicacion 

from config import config
from app import init_app
from app.route.Api_task import mail

from dotenv import load_dotenv
load_dotenv()

configurationdeve = config['development']
configurationprod = config['production']


print(configurationdeve.PORT, configurationdeve.SECRET_KEY )


app = init_app(configurationdeve)
mail.init_app(app)


if __name__ == '__main__':
    app.run(port=configurationdeve.PORT, host=configurationdeve.HOST)



