from flask import Flask, request, jsonify, render_template
import json
import sqlite3

app = Flask(__name__)

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect('images.sqlite')
    except sqlite3.error as e:
        print(e)
    return conn

@app.route("/images", methods=["GET", "POST"])
def images():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == "GET":
        cursor = conn.execute("SELECT * FROM images")
        images = [
            dict(id=row[0], name=row[1], description=row[2], url=row[3])
            for row in cursor.fetchall()
        ]
        if images is not None:
            return jsonify(images)

    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        url = request.form["url"]

        sql = """INSERT INTO images (name, description, url)
                 VALUES (?, ?, ?) """

        cursor = cursor.execute(sql, (name, description, url))
        conn.commit()
        return f"Image with id: {cursor.lastrowid} created successfully"

@app.route('/image/<int:id>', methods=["GET", "PUT", "DELETE"])
def image(id):
    conn = db_connection()
    cursor = conn.cursor()
    image = None

    if request.method == "GET":
        cursor.execute("SELECT * FROM images WHERE id=?", (id,))
        rows = cursor.fetchall()
        for row in rows:
            image = row
        if image is not None:
            return jsonify(dict(id=image[0], name=image[1], description=image[2], url=image[3])), 200
        else:
            return "Image not found", 404

    if request.method == "PUT":
        sql = """UPDATE images SET name = ?, description = ?, url = ?
                 WHERE id = ?"""

        name = request.form["name"]
        description = request.form["description"]
        url = request.form["url"]

        updated_image = {
            "id": id,
            "name": name,
            "description": description,
            "url": url
        }

        conn.execute(sql, (name, description, url, id))
        conn.commit()
        return jsonify(updated_image)

    if request.method == "DELETE":
        sql = """DELETE FROM images WHERE id=?"""
        conn.execute(sql, (id,))
        conn.commit()
        return f"The image with id: {id} has been deleted.", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
