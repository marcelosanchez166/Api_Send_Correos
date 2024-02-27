from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from app.database.db_mysql import get_connection
from app.emails import confirmacion_mail
from flask import current_app



#Mail
from flask_mail import Mail

# print(current_app, "Imprimiendo la aplicacion actual")



mail=Mail()
print(mail, "instancia de Email")

ApiRestfull = Blueprint("ApiRestfull", __name__, url_prefix="/api/v1")

@ApiRestfull.route("/get_tasks_send_mail/<int:id_usuario>")
def get_tasks_send_mail(id_usuario):
    print(id_usuario)
    connection = get_connection()
    with connection.cursor() as cursor: 
        cursor.execute(" SELECT  id_usuario FROM usuarios WHERE id_usuario = %s", (id_usuario, ))
        row2 = cursor.fetchone()
        print(row2[0], "Validando si el id del usuario existe")
        if row2 == id_usuario:
            print(connection.host, connection.password, connection.user, connection.db)
            # El id_usuario debo obtenerlo de la sesion de la aplicacion de tareas para poder usarlo aca 
            sql = """ SELECT  id, nombre_tarea, estado, id_usuario FROM tareas WHERE id_usuario = {}""".format(id_usuario)
            cursor.execute(sql)
            row = cursor.fetchall()
            print(row[0], row[1], row[2], row[3])
            data = []
            for row in row:
                task = {"id": str(row[0]), "nombre_tarea": row[1], "estado": row[2], "id_usuario" : row[3]}
                if row[2] == "Pending":
                    data.append(task)
        #Si solo voy a traer una tarea si puedo usarlo de esta forma pero en el cursor deberia de ser cursor.fetchone() para solo traer una tarea dependiendo del id del usuario
        # data = {"id": row[0], "nombre_tarea": row[1], "estado": row[2], "id_usuario": row[3]}
            
        # Creando instancia del metodo confirmacion_compra del archivo emails, para poder pasarle los valores que espera, que son la instancia de flask que es la app(current_app)
        # la instancia del metodo EMAIL() que se creo arriba, el usuario actual que debo obtenerlo de alguna manera cuando se haga click en el boton, 
        #y las tareas que tambien debo obtener antes para poder enviarlas
        sql = """ SELECT  id, username, password, email FROM usuarios WHERE id = {}""".format(id_usuario)
        cursor.execute(sql)
        row1 = cursor.fetchone()
        print(mail.state, "Instancia mail")
        confirmacion_mail( mail, row1, data)#Este es un envio de correo asincrono
        return jsonify(data)





@ApiRestfull.route("/add_task", methods=["POST"])
def  add_task():
    if request.method == 'POST':
        try:
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
        except Exception as e:
            response={'error':'Error adding the task to the database'}
        
        finally:

            return jsonify(response)    
    


@ApiRestfull.route('/update_task/<int:id>', methods= ['PUT'])
def update_task(id):
    if request.method=='PUT':
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
