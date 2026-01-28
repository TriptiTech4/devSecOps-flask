from flask import Flask

import mysql.connector

import os

import time



app = Flask(__name__)



def get_db_connection():

    """

    Create a MySQL database connection.

    Docker Compose service name 'mysql' is used as host.

    """

    return mysql.connector.connect(

        host=os.getenv("DB_HOST", "mysql"),

        user=os.getenv("DB_USER", "root"),

        password=os.getenv("DB_PASSWORD", "root"),

        database=os.getenv("DB_NAME", "testdb")

    )



@app.route("/")

def home():

    # Retry logic because MySQL may start after Flask

    retries = 5

    while retries > 0:

        try:

            conn = get_db_connection()

            cursor = conn.cursor()

            cursor.execute("SELECT 'DevSecOps Flask App Running on Port 7000'")

            result = cursor.fetchone()

            cursor.close()

            conn.close()

            return str(result)

        except Exception as e:

            retries -= 1

            time.sleep(2)



    return "Database not ready, please refresh in a few seconds", 500

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=7000)
