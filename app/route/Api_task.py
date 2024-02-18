from flask import Blueprint, request, render_template, redirect, url_for, jsonify
# Database
from app.database.db_mysql import get_connection

#Mail
from flask_mail import Mail
from flask import current_app


mail=Mail()

ApiRestfull = Blueprint("ApiRest", __name__, url_prefix="/api/v1")

@ApiRestfull.route("/get_data/<int:id_usuario>", methods=["GET"])
def get_data(id_usuario):
    connection = get_connection()
    with connection.cursor() as cursor:
        # El id_usuario debo obtenerlo de la sesion de la aplicacion de tareas para poder usarlo aca 
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


        # Creando instancia del metodo confirmacion_compra del archivo emails, para poder pasarle los valores que espera, que son la instancia de flask que es la app(current_app)
        # la instancia del metodo EMAIL() que se creo arriba, el usuario actual que debo obtenerlo de alguna manera cuando se haga click en el boton, 
        #y las tareas que tambien debo obtener antes para poder enviarlas
        #confirmacion_compra(current_app, mail, current_user, tareas)#Este es un envio de correo asincrono """
