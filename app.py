from flask import Flask, request, jsonify
from passlib.hash import sha256_crypt

import pymysql
import boto3
import os

app = Flask(__name__)

# Connect to Linode's managed database
conn = pymysql.connect(
    host='lin-16251-9474-mysql-primary-private.servers.linodedb.net',
    user='linroot',
    password=os.environ.get('DB_PASSWORD'),
    ssl_ca='my-cluster-ca-certificate.crt',
    db='wander_xp',
)

# TODO: Add proper user authentication with the SQL DB
@app.route("/register", methods=['POST'])
def register():
    # Create user object to insert into SQL
    passwd1 = request.form.get('password1')
    hashed_pass = sha256_crypt.encrypt(str(passwd1))

    new_user = User(
        username=request.form.get('username'),
        email=request.form.get('username'),
        password=hashed_pass)

    if user_exsists(new_user.username, new_user.email):
        flash('User already exsists!', 'danger')
        return render_template('register.html')
    else:
        # Insert new user into SQL
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        flash('Account created!', 'success')
        return redirect(url_for('index'))


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
def user_exsists(username, email):
    # Get all Users in SQL
    users = User.query.all()
    for user in users:
        if username == user.username or email == user.email:
            return True

    # No matching user
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
    cursor = conn.cursor()
    # Store data in Linode's managed database
    sql = "INSERT INTO data (name, email, message) VALUES (%s, %s, %s)"
    cursor.execute(sql, (data['name'], data['email'], data['message']))
    conn.commit()
    # Store relevant photos and documents in Linode's object storage
    if 'photo' in data:
        s3.upload_file(data['photo'], 'bucket_name', 'photo.jpg')
    if 'document' in data:
        s3.upload_file(data['document'], 'bucket_name', 'document.pdf')
    return jsonify({'message': 'Data stored successfully!'})


@app.route('/get_data', methods=['GET'])
def get_data():
    cursor = conn.cursor()
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
