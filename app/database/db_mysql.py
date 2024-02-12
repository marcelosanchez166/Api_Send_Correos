from decouple import  config
import pymysql
from flask import flash


def get_connection():
    try:
        return pymysql.connect(
            host=config('MYSQL_HOST'),
            user=config('MYSQL_USER'),
            password=config('MYSQL_PASSWORD'),
            db=config('MYSQL_DB')
        )
    except Exception as ex:
        flash(f'Error connecting to MySQL database: {ex}', 'error')
        raise SystemExit(1)