from flask import Flask, request, jsonify, render_template
import mysql.connector
import bcrypt
from config import DB_CONFIG
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

@app.route('/')
def home():
    return render_template('login.html')

# REGISTER API
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json

        name = data['name']
        email = data['email']
        password = data['password']

        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

        db = get_db()
        cursor = db.cursor()

        query = """
        INSERT INTO users (name, email, password)
        VALUES (%s, %s, %s)
        """

        cursor.execute(query, (name, email, hashed_password))
        db.commit()

        return jsonify({"message": "User registered successfully"})

    except mysql.connector.IntegrityError:
        return jsonify({
            "message": "Email already registered"
        }), 400

    except Exception as e:
        return jsonify({
            "message": str(e)
        }), 500
# LOGIN API  👈 MUST BE HERE
@app.route('/login', methods=['POST'])
def login():

    try:
        data = request.json

        email = data['email']
        password = data['password']

        db = get_db()
        cursor = db.cursor(dictionary=True)

        query = "SELECT * FROM users WHERE email=%s"

        cursor.execute(query, (email,))

        user = cursor.fetchone()

        cursor.close()
        db.close()

        if user and bcrypt.checkpw(
            password.encode('utf-8'),
            user['password'].encode('utf-8')
        ):

            return jsonify({
                "message": "Login successful",
                "user": {
                    "id": user['id'],
                    "name": user['name'],
                    "email": user['email']
                }
            })

        return jsonify({
            "message": "Invalid email or password"
        }), 401

    except Exception as e:
        print("LOGIN ERROR:", e)

        return jsonify({
            "error": str(e)
        }), 500
 # ADD TASK API
@app.route('/add_task', methods=['POST'])
def add_task():
    data = request.json

    user_id = data['user_id']
    task_title = data['task_title']
    description = data['description']
    due_date = data['due_date']

    db = get_db()
    cursor = db.cursor()

    query = """
    INSERT INTO tasks (user_id, task_title, description, due_date)
    VALUES (%s, %s, %s, %s)
    """

    cursor.execute(query, (user_id, task_title, description, due_date))
    db.commit()

    return jsonify({"message": "Task added successfully"})

# GET TASKS API
@app.route('/get_tasks/<int:user_id>', methods=['GET'])
def get_tasks(user_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    query = "SELECT * FROM tasks WHERE user_id=%s"
    cursor.execute(query, (user_id,))

    tasks = cursor.fetchall()

    return jsonify(tasks)

# UPDATE TASK STATUS
@app.route('/update_task/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    status = data['status']

    db = get_db()
    cursor = db.cursor()

    query = "UPDATE tasks SET status=%s WHERE id=%s"
    cursor.execute(query, (status, task_id))
    db.commit()

    return jsonify({"message": "Task updated successfully"})

# DELETE TASK API
@app.route('/delete_task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    db = get_db()
    cursor = db.cursor()

    query = "DELETE FROM tasks WHERE id=%s"
    cursor.execute(query, (task_id,))
    db.commit()

    return jsonify({"message": "Task deleted successfully"})


@app.route('/register_page')
def register_page():
    return render_template('register.html')

@app.route('/login_page')
def login_page():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# ALWAYS LAST
if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True)