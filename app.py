from flask import Flask, request, jsonify
from passlib.hash import sha256_crypt

import pymysql
import boto3
import os
import uuid

# environment variables
DB_PASSWORD = os.environ.get('DB_PASSWORD')
OBJECT_STORAGE_KEY_ID = os.environ.get('OBJECT_STORAGE_KEY_ID')
OBJECT_STORAGE_KEY_SECRET = os.environ.get('OBJECT_STORAGE_KEY_SECRET')
# Object storage configuration
OBJECT_STORAGE_CLUSTER_URL = "wander-xp-files.ap-south-1.linodeobjects.com"
BUCKET_NAME = "wander-xp-files"
# SQL queries
SQL_INSERT_USER = "INSERT INTO users (uid, name, email, password, photo_url) VALUES (%s, %s, %s, %s, %s)"
SQL_CHECK_IF_USER_EXISTS = "SELECT * FROM users WHERE email = %s"
SQL_GET_USER_PASSWORD_HASH = "SELECT password FROM users WHERE email = %s"
SQL_GET_TRIPS = "SELECT * FROM trips WHERE uid = %s"
SQL_GET_TRIP = "SELECT * FROM trips WHERE id = %s"
SQL_INSERT_TRIP = "INSERT INTO trips (id, uid, place_name, start_date, end_date, flight_number_arrival, flight_number_departure, hotel_name, hotel_address, hotel_phone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
SQL_UPDATE_TRIP = "UPDATE trips SET place_name = %s, start_date = %s, end_date = %s, flight_number_arrival = %s, flight_number_departure = %s, hotel_name = %s, hotel_address = %s, hotel_phone = %s WHERE id = %s"
SQL_GET_PLACES_TO_VISIT = "SELECT * FROM places_to_visit WHERE trip_id = %s"
SQL_INSERT_PLACES_TO_VISIT = "INSERT INTO places_to_visit (id, trip_id, uid, name, note) VALUES (%s, %s, %s, %s, %s)"
SQL_UPDATE_PLACES_TO_VISIT = "UPDATE places_to_visit SET name = %s, note = %s WHERE id = %s"

app = Flask(__name__)

# Connect to Linode's managed database
db = pymysql.connect(
    host='lin-16251-9474-mysql-primary-private.servers.linodedb.net',
    user='linroot',
    password=DB_PASSWORD,
    ssl_ca='my-cluster-ca-certificate.crt',
    db='wander_xp',
)

# Registering a new user
@app.route("/register", methods=['POST'])
def register():
    data = request.get_json()

    is_already_registered = user_exists(data['email'])
    if is_already_registered:
        return jsonify({'message': 'You are already registered'})

    cursor = db.cursor()

    # Create user object to insert into SQL
    uid = str(uuid.uuid4())
    name = data['name']
    email = data['email']
    password = data['password']
    photo_url = data['photo_url']
    hashed_pass = sha256_crypt.encrypt(str(password))

    if name != '' and email != '' and password != '':
        try:
            # Store user in SQL
            cursor.execute(SQL_INSERT_USER,
                           (uid, name, email, hashed_pass, photo_url))
            db.commit()
        except:
            return jsonify({
                'status': 'ERROR',
                'message': 'Failed to create account'})
    else:
        return jsonify({
            'status': 'ERROR',
            'message': 'Please fill in all fields'})

    cursor.close()
    return jsonify({
        'status': 'SUCCESS',
        'message': 'Account created successfully!'})


# Logging in a user
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data['email']
    password = data['password']

    if email != '' and password != '':
        try:
            cursor = db.cursor()
            cursor.execute(SQL_GET_USER_PASSWORD_HASH, (email))
            results = cursor.fetchall()
            cursor.close()

            if len(results) > 0:
                if sha256_crypt.verify(password, results[0][0]):
                    return jsonify({
                        'status': 'SUCCESS',
                        'message': 'Logged in successfully!'})
                else:
                    return jsonify({
                        'status': 'ERROR',
                        'message': 'Incorrect password!'})
            else:
                return jsonify({'message': 'User does not exist!'})
        except:
            return jsonify({
                'status': 'ERROR',
                'message': 'Failed to login!'})
    else:
        return jsonify({
            'status': 'ERROR',
            'message': 'Please fill in all fields'})

# Fetching a trip by id
@app.route('/trips/<trip_id>', methods=['GET'])
def get_trip(trip_id):
    if trip_id == '':
        return jsonify({
            'status': 'ERROR',
            'message': 'Please provide a valid trip id'})
    try:
        cursor = db.cursor()
        cursor.execute(SQL_GET_TRIP, (trip_id))
        result = cursor.fetchall()[0]
        trip = {
            'id': result[0],
            'uid': result[1],
            'place_name': result[2],
            'start_date': result[3],
            'end_date': result[4],
            'flight_number_arrival': result[5],
            'flight_number_departure': result[6],
            'hotel_name': result[7],
            'hotel_address': result[8],
            'hotel_phone': result[9],
        }
        cursor.execute(SQL_GET_PLACES_TO_VISIT, (trip_id))
        places_to_visit_list = cursor.fetchall()
        places_to_visit = []
        for row in places_to_visit_list:
            places_to_visit.append({
                'id': row[0],
                'trip_id': row[1],
                'uid': row[2],
                'name': row[3],
                'note': row[4]
            })
        trip['places_to_visit'] = places_to_visit
        cursor.close()
        return jsonify({'status': 'SUCCESS', 'trip': trip})
    except:
        return jsonify({
            'status': 'ERROR',
            'message': 'Failed to fetch trip!'})

# Updating a trip by id
@app.route('/trips/<trip_id>/update', methods=['POST'])
def update_trip(trip_id):
    data = request.get_json()
    if trip_id == '':
        return jsonify({
            'status': 'ERROR',
            'message': 'Please provide a valid trip id'})
    try:
        cursor = db.cursor()
        cursor.execute(SQL_UPDATE_TRIP,
                       (data['place_name'], data['start_date'],
                        data['end_date'], data['flight_number_arrival'],
                        data['flight_number_departure'], data['hotel_name'],
                        data['hotel_address'], data['hotel_phone'], trip_id))
        db.commit()
        cursor.close()
        return jsonify({'status': 'SUCCESS', 'message': 'Trip updated!', 'trip_id': trip_id})
    except:
        return jsonify({
            'status': 'ERROR',
            'message': 'Failed to update trip!'})

### @GET: Fetching all trips for a user
### @POST: Creating a new trip for a user
@app.route('/trips', methods=['GET', 'POST'])
def trips():
    data = request.get_json()
    if request.method == 'GET':
        uid = data['uid']
        if (uid == ''):
            return jsonify({
                'status': 'ERROR',
                'message': 'Please provide a valid user id'})
        try:
            cursor = db.cursor()
            cursor.execute(SQL_GET_TRIPS, (uid))
            results = cursor.fetchall()
            cursor.close()
            trips = []
            for row in results:
                trips.append({
                    'id': row[0],
                    'uid': row[1],
                    'place_name': row[2],
                    'start_date': row[3],
                    'end_date': row[4],
                    'flight_number_arrival': row[5],
                    'flight_number_departure': row[6],
                    'hotel_name': row[7],
                    'hotel_address': row[8],
                    'hotel_phone': row[9],
                })

            return jsonify({'status': 'SUCCESS', 'trips': trips})
        except:
            return jsonify({
                'status': 'ERROR',
                'message': 'Failed to fetch trips!'})
    elif request.method == 'POST':
        uid = data['uid']
        trips = data['trips']
        trip_id = str(uuid.uuid4())
        if (uid == '' and trips == None):
            return jsonify({
                'status': 'ERROR',
                'message': 'Please provide a valid user id and trip details'
            })
        # trip details
        place_name = trips['place_name']
        start_date = trips['start_date']
        end_date = trips['end_date']
        flight_number_arrival = trips['flight_number_arrival']
        flight_number_departure = trips['flight_number_departure']
        hotel_name = trips['hotel_name']
        hotel_address = trips['hotel_address']
        hotel_phone = trips['hotel_phone']
        places_to_visit_id = str(uuid.uuid4())
        # places to visit
        places_to_visit_name = trips['places_to_visit'][0]['name']
        places_to_visit_note = trips['places_to_visit'][0]['note']
        cursor = db.cursor()
        # Store trip in SQL
        cursor.execute(SQL_INSERT_TRIP,
                       (trip_id, uid, place_name, start_date, end_date,
                        flight_number_arrival, flight_number_departure,
                        hotel_name, hotel_address, hotel_phone))
        db.commit()
        cursor.execute(SQL_INSERT_PLACES_TO_VISIT,
                       (places_to_visit_id,
                        trip_id,
                        uid,
                        places_to_visit_name,
                        places_to_visit_note))
        db.commit()
        return jsonify({
            'status': 'SUCCESS', 'message': 'Trip created successfully!', 'trip_id': trip_id})


# Check if username or email are already taken
def user_exists(email):
    try:
        cursor = db.cursor()
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
linode_obj_config = {
    "aws_access_key_id": OBJECT_STORAGE_KEY_ID,
    "aws_secret_access_key": OBJECT_STORAGE_KEY_SECRET,
    "endpoint_url": OBJECT_STORAGE_CLUSTER_URL,
}
s3 = boto3.client('s3',**linode_obj_config)
s3 = boto3.resource('s3')

@app.route('/store_file', methods=['POST'])
def store_file():
    data = request.get_json()
    # Need to pass file, file_name, file_type
    if 'file' in data:
        unique_str = str(uuid.uuid4())
        file_name = data['file_name'] + f"_{unique_str}"+ '.' + data['file_type']
        try:
            s3.upload_file(data['file'], BUCKET_NAME, file_name)
            return jsonify({
                'status': 'SUCCESS',
                'message': 'File stored successfully!', 'file_name': file_name})
        except:
            return jsonify({
                'status': 'ERROR',
                'message': 'Failed to store file!'})

@app.route('/get_file', methods=['GET'])
def get_file():
    data = request.get_json()
    # Need to pass file_name
    if 'file_name' in data:
        try:
            file = s3.download_file(BUCKET_NAME, data['file_name'], data['file_name'])
            return jsonify({
                'status': 'SUCCESS',
                'message': 'File retrieved successfully!', 'file_name': data['file_name'], 'file': file})
        except:
            return jsonify({
                'status': 'ERROR',
                'message': 'Failed to retrieve file!'})



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
