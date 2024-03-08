from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from app.database.db_mysql import get_connection
from app.emails import confirmacion_mail
from flask import current_app

import jwt
from jwt import encode, decode




#Mail
from flask_mail import Mail
# print(current_app, "Imprimiendo la aplicacion actual")


mail=Mail()
print(mail, "instancia de Email")


ApiRestfull = Blueprint("ApiRestfull", __name__, url_prefix="/api/v1")


@ApiRestfull.route("/get_tasks_send_mail/<int:id_usuario>", methods= [ 'GET'])  # ,'GET','PUT
# @token_required
def get_tasks_send_mail(id_usuario):
    print(id_usuario)
    # Verificar si el token está presente en el encabezado de autorización
    authorization_token = request.headers.get('Authorization')
    if request.method == 'GET':
        if authorization_token :
            print(authorization_token, "Imprimiendo el token ")
            encoded_token = authorization_token.split(" ")[1]
            if (len(encoded_token) > 0):
                try:
                    payload = jwt.decode(encoded_token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
                    # Si el token está presente, continuar con la lógica de autenticación y obtención de tareas
                    connection = get_connection()
                    with connection.cursor() as cursor: 
                        cursor.execute("SELECT id FROM usuarios WHERE id = %s", (id_usuario,))
                        row2 = cursor.fetchone()
                        if row2 is not None and len(row2) > 0:
                            print(connection.host, connection.password, connection.user, connection.db)
                            sql = """SELECT id, nombre_tarea, estado, id_usuario FROM tareas WHERE id_usuario = {}""".format(id_usuario)
                            cursor.execute(sql)
                            rows = cursor.fetchall()
                            data = []
                            for row in rows:
                                task = {"id": str(row[0]), "nombre_tarea": row[1], "estado": row[2], "id_usuario": row[3]}
                                if row[2] == "Pending":
                                    data.append(task)
                            # Obtener detalles del usuario para enviar por correo electrónico
                            sql = """SELECT id, username, password, email FROM usuarios WHERE id = {}""".format(id_usuario)
                            cursor.execute(sql)
                            user_details = cursor.fetchone()
                            # Enviar correo electrónico de confirmación
                            confirmacion_mail(mail, user_details, data)  # Este es un envío de correo asíncrono
                            return jsonify(data)
                        else:
                            return jsonify({"Id": "user id does not exist"})
                except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
                    return jsonify({"message": "Token is expired!"}), 403
            else: 
                return  jsonify({"message": "Token is missing!"}), 403
        return jsonify({"message": "Token is missing!"}), 403
    else:
        return jsonify({"message":"Request method must be GET"}), 405



@ApiRestfull.route("/add_task", methods=["POST"])
#@token_required
def  add_task():
    authorization_token = request.headers.get('Authorization')
    # print(authorization_token, "Imprimiendo el token ")
    if request.method == 'POST':
        #if token:
        if authorization_token :
            print(authorization_token, "Imprimiendo el token ")
            encoded_token = authorization_token.split(" ")[1]
            if (len(encoded_token) > 0):
                try:
                    payload = jwt.decode(encoded_token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
                    nombre_tarea = request.json['nombre_tarea']
                    estado_tarea = request.json['estado']
                    id_usuario   = request.json['id_usuario']
                    print(request.json)
                    connection = get_connection()
                    with connection.cursor() as cursor:
                        sql = """INSERT INTO tareas (nombre_tarea, estado, id_usuario) VALUES(%s,%s,%s)"""
                        cursor.execute(sql,(nombre_tarea, estado_tarea, id_usuario))
                        connection.commit()
                        response= {'message':'Task added correctly'}
                        return jsonify(response), 201
                except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
                    response={'error':'Error adding the task to the database'}
                    return jsonify({"message": "Token is expired!", "response":response}), 403
                # finally:
                #     return jsonify(response)
            else: 
                return  jsonify({"message": "Token is missing!"}), 403
        else:
            return jsonify({"message": "Token is missing!"}), 403
    else:
        return jsonify({"message":"Request method must be POST"}), 405


@ApiRestfull.route('/update_task/<int:id>', methods= ['PUT'])
#@token_required
def update_task(id):
    authorization_token = request.headers.get('Authorization')
    print(authorization_token, "Imprimiendo el token ")
    if request.method == 'PUT':
        if authorization_token:
            print(authorization_token, "Imprimiendo el token ")
            encoded_token = authorization_token.split(" ")[1]
            if (len(encoded_token) > 0):
                try:
                    payload = jwt.decode(encoded_token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
                    # id_tarea = request.args.get('id')
                    nombre_nuevo = request.json['new_name']
                    nuevo_estado = request.json['new_status']
                    print("Nombre Nuevo",nombre_nuevo,"Estado Nuevo",nuevo_estado)
                    #Verificar que los campos  no esten vacios
                    if all([nombre_nuevo,nuevo_estado]):
                        connection = get_connection()
                        with connection.cursor() as cursor:
                            #sql = """UPDATE `tareas` SET `nombre_tarea`='{}',`estado`='{}' WHERE id = '{}'""".format(nombre_nuevo, nuevo_estado, id)
                            #cursor.execute(sql)
                            cursor.execute("UPDATE `tareas` SET `nombre_tarea`= %s,`estado`= %s WHERE id = %s", (nombre_nuevo, nuevo_estado, id ))
                            connection.commit()
                            response= {'message':'Task updated correctly'}
                        # respuesta = update_task(nombre_nuevo,nuevo_estado)
                        return jsonify({ "response": response})
                    else :
                        return jsonify({"error":"All fields must be filled out."})
                except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
                    return jsonify({"message": "Token is expired!"}, ), 403
            else: 
                return  jsonify({"message": "Token is missing!"}), 403
        else:
            return {"message": "You do not have permission to perform this action, verify the token"}
    else:
        return {"message": "Unauthorized access"}, 401



@ApiRestfull.route("/delete_task/<int:id>", methods=["DELETE"])
def delete_task(id):
    print(id, "Id para eliminar tareas")
    authorization_token = request.headers.get('Authorization')
    print(authorization_token, "Imprimiendo el token ")
    if request.method == 'DELETE':
        if authorization_token:
            print(authorization_token, "Imprimiendo el token ")
            encoded_token = authorization_token.split(" ")[1]
            if (len(encoded_token) > 0):
                try:
                    payload = jwt.decode(encoded_token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
                    if id :
                        connection = get_connection()
                        with connection.cursor() as cursor:
                            cursor.execute("SELECT  id FROM  tareas  WHERE id = %s", (id, ))
                            result = cursor.fetchone()
                            if  result  is not None and len(result) > 0:
                                cursor.execute("DELETE FROM  tareas  WHERE id = %s", (id, ))
                                connection.commit()
                                response= {'message':'Task deleted correctly'}
                                return jsonify(response)
                            else:
                                return jsonify({"message":"The task does not exist"}), 404
                except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
                    return jsonify({"message": "Token is expired!"}, ), 403
            else:
                return  jsonify({"message": "Token is missing!"}), 403
        else:
            return {"message": "You do not have permission to perform this action, verify the token"}
    else:
        return {"message": "Unauthorized access"}, 401




