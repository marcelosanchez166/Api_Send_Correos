from flask import Blueprint, request, render_template, redirect, url_for, jsonify
# Database
from app.database.db_mysql import get_connection

ApiRestfull = Blueprint("ApiRestfull", __name__, url_prefix="/api/v1")

@ApiRestfull.route("/get_data/<int:id_usuario>", methods=["GET"])
def get_data(id_usuario):
    connection = get_connection()
    with connection.cursor() as cursor:
        sql = """ SELECT  id, nombre_tarea, estado, id_usuario FROM tareas WHERE id_usuario = {}""".format(id_usuario)
        cursor.execute(sql)
        row = cursor.fetchall()
        print(row[0], row[1], row[2], row[3])
        data = []
        for row in row:
            task = {"id": str(row[0]), "nombre_tarea": row[1], "estado": row[2], "id_usuario" : row[3]}
            data.append(task)
        #Si solo voy a traer una tarea si puedo usarlo de esta forma pero en el cursor deberia de ser cursor.fetchone() para solo traer una tarea dependiendo del id del usuario
        # data = {"id": row[0], "nombre_tarea": row[1], "estado": row[2], "id_usuario": row[3]}
        return jsonify( data)


