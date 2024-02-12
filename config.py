#El metodo config de decouple sirve para trabajar con variables de entorno y se complementa con  la biblioteca python-dotenv 

#python-dotenv Nos va ayudar a leer valores de tipo clave valor para poder utilizarlos como variables de entorno desde el archivo .env que creamos.

#python-decouple para manejar la configuración de una aplicación de manera más segura y flexible separando la configuración del código fuente, 
#se accede atravez del metodo config que si le pasamos un valor obtenemos la varible que hemos definido en el archivo .env

#instalacion de decouple para usar el metodo config pip install python-decouple y python-dotenv
from decouple import config


#en este caso importamos decouple para hacer uso de la variable SECRET_KEY accediendo atravez del metodo config("SECRET_KEY") y dicha valor lo guardo en una variable llamada SECRET_KEY
class Config():
    SECRET_KEY = config('SECRET_KEY')

class DevelopmentConfig(Config):
    DEBUG = True
    PORT=5001
    HOST= "0.0.0.0"
    MAIL_SERVER=config("MAIL_SERVER")#Simple Mail Transfer Protocol
    MAIL_PORT=config("MAIL_PORT") #Puerto de google TLS
    MAIL_USE_TLS=config("MAIL_USE_TLS")
    MAIL_USERNAME=config("MAIL_USERNAME")
    MAIL_PASSWORD=config("MAIL_PASSWORD")#Usando el metodo config de la libreria decouple para no poner la password como tal a nivel de codigo si no que se creara un archivo llamado .env para poner ese tipo de variables 



class ProductionConfig(Config):
    # DEBUG = True
    PORT="5001"
    HOST= "0.0.0.0"
    MAIL_SERVER=config("MAIL_SERVER")#Simple Mail Transfer Protocol
    MAIL_PORT=config("MAIL_PORT") #Puerto de google TLS
    MAIL_USE_TLS=config("MAIL_USE_TLS")
    MAIL_USERNAME=config("MAIL_USERNAME")
    MAIL_PASSWORD=config("MAIL_PASSWORD")#Usando el metodo config de la libreria decouple para no poner la password como tal a nivel de codigo si no que se creara un archivo llamado .env para poner ese tipo de variables 


#Luego instancio el metodo config para pasarle la clases de produccion y la de desarrollo para que dependiendo de donde se vaya a desplegar sea usada la clase correspondiente
config = {
    'development': DevelopmentConfig,
    "production" : ProductionConfig
}