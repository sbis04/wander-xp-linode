from flask import Flask, request, jsonify
from passlib.hash import sha256_crypt

import pymysql
import boto3
import os

# constants
DB_PASSWORD = os.environ.get('DB_PASSWORD')
SQL_INSERT_USER = "INSERT INTO users (name, email, password, photo_url) VALUES (%s, %s, %s, %s)"
SQL_CHECK_IF_USER_EXISTS = "SELECT * FROM users WHERE email = %s"

app = Flask(__name__)

# Connect to Linode's managed database
db = pymysql.connect(
    host='lin-16251-9474-mysql-primary-private.servers.linodedb.net',
    user='linroot',
    password=DB_PASSWORD,
    ssl_ca='my-cluster-ca-certificate.crt',
    db='wander_xp',
)
cursor = db.cursor()

# TODO: Add proper user authentication with the SQL DB


@app.route("/register", methods=['POST'])
def register():
    data = request.get_json()

    is_already_registered = user_exists(data['email'])
    if is_already_registered:
        return jsonify({'message': 'You are already registered'})

    # Create user object to insert into SQL
    password = data['password']
    hashed_pass = sha256_crypt.encrypt(str(password))

    try:
        # Store user in SQL
        cursor.execute(
            SQL_INSERT_USER, (data['name'], data['email'], data['message'], data['photo_url']))
        db.commit()
    except:
        db.rollback()

    db.close()


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password_candidate = request.form.get('password')

    # Query for a user with the provided username
    result = User.query.filter_by(username=username).first()

    # If a user exsists and passwords match - login
    if result is not None and sha256_crypt.verify(password_candidate, result.password):
        # Init session vars
        login_user(result)
        flash('Logged in!', 'success')
        return redirect(url_for('index'))
    else:
        flash('Incorrect Login!', 'danger')
        return render_template('login.html')


@app.route("/logout")
def logout():
    logout_user()
    flash('Logged out!', 'success')
    return redirect(url_for('index'))


# Check if username or email are already taken
def user_exists(email):
    try:
        # Store user in SQL
        cursor.execute(SQL_CHECK_IF_USER_EXISTS, (email))
        results = cursor.fetchall()
    except:
        db.rollback()
    
    if len(results) > 0:
        return True
    else:
        return False


# Connect to Linode's object storage
s3 = boto3.client('s3',
                  aws_access_key_id='access_key',
                  aws_secret_access_key='secret_key'
                  )


@app.route('/')
def index():
    return 'Welcome to the Wander XP API!'


@app.route('/store_data', methods=['POST'])
def store_data():
    data = request.get_json()
    cursor = db.cursor()
    # Store data in Linode's managed database
    sql = "INSERT INTO data (name, email, message) VALUES (%s, %s, %s)"
    cursor.execute(sql, (data['name'], data['email'], data['message']))
    db.commit()
    # Store relevant photos and documents in Linode's object storage
    if 'photo' in data:
        s3.upload_file(data['photo'], 'bucket_name', 'photo.jpg')
    if 'document' in data:
        s3.upload_file(data['document'], 'bucket_name', 'document.pdf')
    return jsonify({'message': 'Data stored successfully!'})


@app.route('/get_data', methods=['GET'])
def get_data():
    cursor = db.cursor()
    # Retrieve data from Linode's managed database
    sql = "SELECT * FROM data"
    cursor.execute(sql)
    result = cursor.fetchall()
    data = []
    for row in result:
        data.append({
            'id': row[0],
            'name': row[1],
            'email': row[2],
            'message': row[3]
        })
    return jsonify({'data': data})


if __name__ == '__main__':
    app.run()
