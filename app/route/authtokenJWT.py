#Librerias necesarias para la creacion y validacion de tokens jwt
from flask import request, jsonify, current_app, Blueprint
import jwt
from jwt import encode, decode
import datetime
from app.database.db_mysql import get_connection

from werkzeug.security import generate_password_hash, check_password_hash #Importando los metodos para encriptar y desencriptar las passwords, metodo para desencriptar(check_password_hash),metodo para encriptar(generate_password_hash)


jwt_token_acces = Blueprint("jwt_token_acces", __name__, url_prefix="/api/v2")


# Ruta para obtener un token de autenticación
@jwt_token_acces.route('/get_jwt_token', methods=["GET"])
def get_jwt():
    # Datos de autenticación (pueden ser obtenidos de una base de datos)
    username = request.json["username"]
    password = request.json["password"]
    #print(username, password, "Entrantes para obtener el token")
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(" SELECT  username, password FROM usuarios WHERE username = %s", (username, ))
        row1 = cursor.fetchone()
        print(row1[0], row1[1], "datos obtenidos desde la base ")
        coincide=check_password_hash(row1[1],password)#Validara que la password sea igual que la del texto que recibio por eso se le pasa la variable encriptado y el valor que tiene password para ver si coinciden
        print(coincide, "Imprimiendo la variable coincide")
        if row1 :
            if coincide :
                # Verificar credenciales (esto es solo un ejemplo)
                # print(request.authorization.username, )
                # if request.authorization and request.authorization.username == row1[0] and request.authorization.password == row1[1]:
                    # Crear token
            #     token = jwt.encode({'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, current_app.config['SECRET_KEY'])
            #     return jsonify({'token': token.decode('UTF-8')})
            # return jsonify({'message': 'Could not verify!'}), 401  # 401: Unauthorized
                # Crear token
                # token = jwt.encode({'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, current_app.config['SECRET_KEY'])
                # return jsonify({'token': token})

                """convertir los objetos datetime a cadenas de texto antes de incluirlos en el payload del token. """
                issued_at = datetime.datetime.utcnow()
                payload = {
                    # 'issued_at': datetime.datetime.utcnow(),
                    'issued_at': issued_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10),
                    'username': username,
                    'password': password
                    }
                # token = jwt.encode({'user': username, 'issued_at' : datetime.datetime.utcnow(), 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, 
                # current_app.config['SECRET_KEY'],algorithm='HS256')
                return jsonify({"token" : jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")})
            return jsonify({'message': 'Could not verify!'}), 401  # 401: Unauthorized
        else:
            return jsonify({'message': 'User not found!'}), 404  # 404: Not Found

